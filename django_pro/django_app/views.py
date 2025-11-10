from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .models import CloudTable
from .serializers import CloudTableSerializer
import json
import cloudinary
import bcrypt



def welcome(request):

    return HttpResponse("Welcome to Mani's app deployed on Render ")


def sample(request):
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
            print(user_email,type(user_email))
            user_email=user_email.encode("utf-8")## to convert str data into byte format
            print(user_email,type(user_email))
            ##bcrypt code
            u_salt=bcrypt.gensalt(rounds=14)   #generate salt     abc123  bcd234  cde345  def456  #4 -32
            # print(u_salt)

            encrypted_email=bcrypt.hashpw(password=user_email,salt=u_salt)## 
            print(encrypted_email,"after hashing" ,type(encrypted_email))

            encrypted_email=encrypted_email.decode("utf-8") ##to convert byte code value into string (for storage)
            print(encrypted_email,"after hashing",type(encrypted_email))



            ##checking password







            img_url=cloudinary.uploader.upload(user_image)

            new_user=CloudTable.objects.create(id=user_id,email=encrypted_email,name=user_name,mob=user_mob,profile_pic=img_url["secure_url"])
            serializer = CloudTableSerializer(new_user)
            return JsonResponse(
                {"msg": "User created successfully!", "user": serializer.data},
                status=201
            )
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




# cloudinary 
# -> to store the media files



# environment -> to isolate  the dependencies (packages and libraries)
#project creation -> django-admin startproject pro_name 
#app creation  -> django-admin startapp app_name   (module or a comp that perform a specific task)
#



#CRUD    -user data
#deployed 

#personal info 
#name mob email  age    password 

#hacking


#sm   app   - share
# credit calls


# data bases




# reg    ->     server      ->  database     mani123     nboj234


#encoding
#encryption
#hashing


#utf-8    unicode transformation format  




# ela unnav     -> english       ->   english  -> hindi



#encryption 




# secret_key="hi"
# msg="how are you?"
# encrypted="how are you"


#hashing

# text="good afternoon"

# algorithm="jhsdfhsdghsdjkfhsdjkh"  ##rsa

# ##irreversible 
# new_text= "good afternoon"  #rsa




#password





# brute force



# 9045


#trying all the possibilities 



# p= 9045
# s=0000
# l=9999


# for i in range(s,l):
#     if i==p:
#         print("your pin is", p)



#bcrypt


# reg_p=123  
# sfgdh



# 123  hash  sfgdh

# post data -> field   -> salt(rounds) for complexity   ->  hashpw(value,salt)  ->   store hashed data



# "$2b$14$Yhz/9ZzqbVKkODG.z4r6ZOIzBCkQaWZNHKrqArstBikyMZf5dyh6u" =="anvesh_bhai@gmail.com"