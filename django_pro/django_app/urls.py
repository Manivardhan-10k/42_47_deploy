from django.urls import path
from . import views

urlpatterns = [
    path('', views.welcome),
    path('sample/', views.sample),
    path('register/', views.reg_user),
    path('users/', views.get_users),
    path('user/<int:id>/', views.get_user_by_id),
    path('update/<int:id>/', views.update_user),
    path('delete/<int:id>/', views.delete_user),
    # path("login/",view=views.login_user),
    # path("send_file/",view=views.send_file)
]
