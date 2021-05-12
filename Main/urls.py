from django.urls import path
from .views import home, logout, login_view

app_name = 'Main'

urlpatterns = [
    path('', home, name='Home'),
    path('login/', login_view, name='Login'),
    path('logout/', logout, name='logout'),
]
