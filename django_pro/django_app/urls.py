from django.urls import path 
from . import views


urlpatterns=[
<<<<<<< HEAD
    path("welcome/",view=views.welcome),
    path("sample/",view=views.sample),
    path("reg_user/",view=views.reg_user)
=======
    path("",view=views.welcome),
    path("sample/",view=views.sample)
>>>>>>> 6e5965822e593e62929b7129b90cdc6c5b21d6c4
]