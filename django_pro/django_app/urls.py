from django.urls import path 
from . import views


urlpatterns=[
    path("welcome/",view=views.welcome),
    path("sample/",view=views.sample)
]