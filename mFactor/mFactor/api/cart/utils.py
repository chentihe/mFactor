import base64
import pickle
from django_redis import get_redis_connection
from mFactor.api.cart import constants

'''
selected:是否勾選此商品
設定cart key value為:(user_id, {sku: [quantity, selected]})
redis 儲存格式是bytes
'''
class CartMixin(object):
    '''設定購物車 CRUD方式'''
    def get_cart(self, request) -> dict:
        user = request.user
        #如果是用戶則讀取redis的資料，如果是訪客則讀取cookie中的資料
        if user and user.is_authenticated:
            return self.get_from_redis(user)
        else:
            return self.get_from_cookie(request)

    def post_cart(self, request, cart_dict, response):
        user = request.user
        #如果是用戶則寫入redis，如果是訪客則寫入cookie中
        if user and user.is_authenticated:
            return self.post_to_redis(request, cart_dict)
        else:
            return self.post_to_cookie(cart_dict, response)

    def get_from_redis(self, request, cart_dict):
        redis_conn = get_redis_connection('cart')
        # redis取出的值為'bytes'
        '''
        順序: str -> bytes -> dict
        base64.b64decode(cart_bytes) 將64進位bytes -> 16進位bytes
        pickle.loads() 轉換 16進位bytes -> dict
        '''
        cart_bytes = redis_conn.get(f'cart_{user.id}')
        cart_dict = pickle.loads(base64.b64decode(cart_bytes)) if cart_bytes else dict()
        return cart_dict

    def post_to_redis(self, request, cart_dict):
        redis_conn = get_redis_connection('cart')
        '''
        順序: dict -> bytes -> str
        pickle.dumps(cart_dict) 將dict -> 16進位bytes
        base64.b64encode() 轉換 16進位bytes -> 64進位bytes
        .decode 解碼成base64_str
        '''
        cart_str = base64.b64encode(pickle.dumps(cart_dict)).decode
        redis_conn.set(f'cart_{request.user.id}', cart_str)

    def get_from_cookie(self, request) -> dict:
        cart_str = request.COOKIES.get('cart') # class:str
        '''
        順序: str -> bytes -> dict
        cart_str.encode() 將base64_str -> 64進位bytes
        base64.b64decode() 轉換 64進位bytes -> 16進位bytes
        pickle.loads() 轉換 16進位bytes -> dict
        '''
        cart_dict = pickle.loads(base64.b64decode(cart_str.encode())) if cart_str else dict()
        return cart_dict

    def post_to_cookie(self, cart_dict, response):
        '''
        順序: dict -> bytes -> str
        pickle.dumps(cart_dict) 將dict -> 16進位bytes
        base64.b64encode() 轉換 16進位bytes -> 64進位bytes
        .decode 解碼成base64_str
        '''
        cart_str = base64.b64encode(pickle.dumps(cart_dict)).decode()
        response.set_cookie('cart', cart_str, max_age=constants.CART_COOKIE_EXPIRES)

def merge_cart_cookie_to_redis(request, user, response):
    merge_cart = CartMixin()
    # 取出用戶在redis的購物車資料
    redis_cart_dict = merge_cart.get_from_redis(user)
    # 取出用戶在未登錄時候的購物車資料
    cookie_cart_dict = merge_cart.get_from_cookie(request)
    '''
    redis_cart_dict.update(cookie_cart_dict)
    將cookie_cart_dict的資料更新到redis_cart_dict
    若key相同會直接覆蓋cookie_cart_dict的值
    '''
    redis_cart_dict.update(cookie_cart_dict)
    # 將資料存進redis中
    merge_cart.post_to_redis(request, redis_cart_dict)
    # 刪除cookie的購物車資料
    response.delete_cookie('cart')

def merge_cart_decoration(func):
    def wrapper(request, *args, **kwargs):
        print('Call original function' + request.method)

        response = func(request, *args, **kwargs)

        if 200 <= response.status_code < 300:
            if request.user and request.user.is_authenticated:
                merge_cart_cookie_to_redis(request, request.user, response)
                print('Merging completed')
            else:
                print('Please add user attr into request if login success')
        else:
            print('Identification Error, merging failed')
        
        return response

    return wrapper
