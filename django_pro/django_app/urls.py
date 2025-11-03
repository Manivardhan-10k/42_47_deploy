from django.urls import path 
from . import views


urlpatterns=[
    path("welcome/",view=views.welcome),
    path("sample/",view=views.sample),
    path("reg_user/",view=views.reg_user)
]