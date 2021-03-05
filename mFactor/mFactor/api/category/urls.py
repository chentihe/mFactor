from rest_framework.routers import DefaultRouter

from ecommerce.api.category.views import CategoryReadOnlyView

router = DefaultRouter
router.register(r'categories', CategoryReadOnlyView)