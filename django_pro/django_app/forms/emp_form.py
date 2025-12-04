from pyexpat import model
from django import forms
from django.forms  import Form  
from ..models import Employees


#general form
#model form


class EmpForm(forms.ModelForm):
    class Meta:
     model=Employees
     fields="__all__"
