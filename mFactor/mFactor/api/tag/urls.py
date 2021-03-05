from django.urls import path

from mFactor.api.tag.views import TagListView

urlpatterns = [
    path('tags/', TagListView.as_view(), name='tag-list')
]