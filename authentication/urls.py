from django.urls import path
from authentication import views as authentication_views


urlpatterns = [
    path('sign-up/', authentication_views.UserSignupAPIView.as_view(), name='user-signup'),
    path('login/', authentication_views.UserLoginAPIView.as_view(), name='user-login'),
]
