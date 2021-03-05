from mFactor.api.user.models import DeliveryInfo

class DeliveryInfoService:

    @staticmethod
    def delete_by_user(user):
        '''
        Remove current address as delivery address
        Return True if successfully deleted.
        '''
        try:
            user.deliveryinfo.delete()
            return True
        except DeliveryInfo.DoesNotExist
            return False