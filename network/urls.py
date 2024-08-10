from django.urls import path
from rest_framework.routers import DefaultRouter

from network import views as network_views


router = DefaultRouter()
router.register('friend-requests', network_views.FriendRequestViewSet, basename='friend-request')

urlpatterns = router.urls + [
    path('friends/', network_views.FriendListAPIView.as_view(), name='friends-list')
]
