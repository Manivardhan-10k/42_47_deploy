from django.http import HttpResponse,JsonResponse
from django.shortcuts import render
import json
from .serializers import CloudTableSerializer
from .models import CloudTable
from django.views.decorators.csrf import csrf_exempt

# Create your views here.


def welcome(req):
    return HttpResponse("welcome to mani's app from render") 

def  sample(req):
    return JsonResponse ({"msg":"json response from render"})


@csrf_exempt
def reg_user(req):
    user_Data=json.loads(req.body)
    #ORM -> Object relational Mapping
    new_user=CloudTable.objects.create(id=user_Data["id"],name=user_Data["name"],email=user_Data["email"],mob=user_Data["mob"])
    return  JsonResponse({"msg":"user created successfully"})






# server->render 
# database -> aiven

# name
# user
# password
# host
# port
