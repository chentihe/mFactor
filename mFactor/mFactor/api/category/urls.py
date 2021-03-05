from rest_framework.routers import DefaultRouter

from mFactor.api.category.views import CategoryReadOnlyView

router = DefaultRouter
router.register(r'categories', CategoryReadOnlyView)