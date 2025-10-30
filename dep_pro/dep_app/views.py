from django.shortcuts import render
from django .http  import HttpResponse

# Create your views here.



def welcome(req):
    return HttpResponse ("welcome to mani's app from render")