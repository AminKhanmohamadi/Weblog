from django.urls import path
from .views import *
urlpatterns = [
    path('singup/' , SingUpView.as_view() , name='singup'),
]