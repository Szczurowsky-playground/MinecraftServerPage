from django.urls import path
from .views import home, logout, login_view, register_view, security

app_name = 'Main'

urlpatterns = [
    path('', home, name='Home'),
    path('login/', login_view, name='Login'),
    path('register/', register_view, name='Register'),
    path('logout/', logout, name='logout'),
    path('security/', security, name='security')
]
