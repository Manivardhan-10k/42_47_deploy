from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .models import CloudTable
from .serializers import CloudTableSerializer
import json
import cloudinary



def welcome(request):

    return HttpResponse("Welcome to Mani's app deployed on Render ")


def sample(request):
    """Simple JSON response to test API"""
    return JsonResponse({"msg": "JSON response from Render"})




@csrf_exempt
def reg_user(request):
    if request.method == "POST":
        try: 
            user_id=request.POST.get("id")
            user_name=request.POST.get("name")
            user_email=request.POST.get("email")
            user_mob=request.POST.get("mob")
            user_image=request.FILES.get("profile")
            img_url=cloudinary.uploader.upload(user_image)
            print(img_url["secure_url"])

            new_user=CloudTable.objects.create(id=user_id,email=user_email,name=user_name,mob=user_mob,profile_pic=img_url["secure_url"])
            
            return JsonResponse({"msg": "User created successfully!","details":list(new_user.values())})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Only POST method allowed"}, status=405)


def get_users(request):
    if request.method == "GET":
        users = CloudTable.objects.all()
        serializer = CloudTableSerializer(users, many=True)
        return JsonResponse(serializer.data, safe=False)
    return JsonResponse({"error": "Only GET method allowed"}, status=405)


def get_user_by_id(request, id):
    if request.method == "GET":
        try:
            user = CloudTable.objects.get(id=id)
            serializer = CloudTableSerializer(user)
            return JsonResponse(serializer.data, safe=False)
        except CloudTable.DoesNotExist:
            return JsonResponse({"error": "User not found"}, status=404)
    return JsonResponse({"error": "Only GET method allowed"}, status=405)


@csrf_exempt
def update_user(request, id):
    if request.method == "PUT":
        try:
            user = CloudTable.objects.get(id=id)
            data = json.loads(request.body)

            user.name = data.get("name", user.name)
            user.email = data.get("email", user.email)
            user.mob = data.get("mob", user.mob)
            user.save()

            serializer = CloudTableSerializer(user)
            return JsonResponse({"msg": "User updated successfully", "user": serializer.data})
        except CloudTable.DoesNotExist:
            return JsonResponse({"error": "User not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Only PUT method allowed"}, status=405)


@csrf_exempt
def delete_user(request, id):
    if request.method == "DELETE":
        try:
            user = CloudTable.objects.get(id=id)
            user.delete()
            return JsonResponse({"msg": "User deleted successfully"})
        except CloudTable.DoesNotExist:
            return JsonResponse({"error": "User not found"}, status=404)
    return JsonResponse({"error": "Only DELETE method allowed"}, status=405)











#cloud database connection
#crud operations  -  reg_user  




#text , images files 




#request.FILES


# server + db  + filehandling


# render +  aiven  +   cloudinary 
#  ec2       rds         s3




# server + db      text  only 
         


#          storage





# account creattion 


# cloudinary 
# api 
# secret