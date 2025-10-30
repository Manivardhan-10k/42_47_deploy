from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.


def welcome(req):
    return HttpResponse("welcome to mani's app from render")