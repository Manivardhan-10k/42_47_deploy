from django.urls import path
from django.views import View
from . import views

# from .views import Sample,EmployeeList,SingleEmp,DelEmp,CreateEmp,UpdateEmp

urlpatterns = [
    path('', views.welcome),
    path('sample/', views.sample),
    path('register/', views.reg_user),
    path('users/', views.get_users),
    path('user/<int:id>/', views.get_user_by_id),
    path('update/<int:id>/', views.update_user),
    path('delete/<int:id>/', views.delete_user),
    path("login/",view=views.login_user),
    path("send_file/",view=views.send_file)


    # path("",view=views.sample_template,name="default"),
    # path("var/",view=views.var_sample,name="var"),
    # path("inherit/",view=views.sample_inherit,name="inherit"),
    # path("loops/",view=views.sample_loop ,name="sample4")




    ##emp table
    # path("getemp/",view=views.emp_table)
    # path("sample/",view=Sample.as_view()),
    # path("emp_list/",view=EmployeeList.as_view(),name="employee_list"),
    # path("emp/<int:pk>/",view=SingleEmp.as_view(),name="emp_details"),
    # path("del_emp/<int:pk>/",view=DelEmp.as_view(),name="del_emp"),
    # ## params - route params
    # path("reg_emp/",view=CreateEmp.as_view(),name="reg_emp"),
    # path("update_emp/<int:pk>/",view=UpdateEmp.as_view(),name="update_emp"),
    # path("emp_pages/",view=views.emp_pages)


]
