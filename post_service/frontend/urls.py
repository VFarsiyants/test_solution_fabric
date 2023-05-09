from django.urls import path, include
from .views import login_page, register, home, logout_user



urlpatterns = [
    path('login/', login_page, name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', register, name='register'),
    path('', home, name='home'),
]