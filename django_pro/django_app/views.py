from django.http import HttpResponse,JsonResponse
from django.shortcuts import render

# Create your views here.


def welcome(req):
    return HttpResponse("welcome to mani's app from render") 

def  sample(req):
    return JsonResponse ({"msg":"json response from render"})