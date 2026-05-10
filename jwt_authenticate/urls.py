from django.urls import path
from .views import Login, Register, Profile

urlpatterns = [
    path('register/', Register.as_view(), name='register-view'),
    path('login/', Login.as_view(), name='login-view'),
    path('profile/', Profile.as_view(), name='profile-view'),
]
