from django.urls import path 
from . import views


urlpatterns=[
    path("",view=views.welcome),
    path("sample/",view=views.sample)
]