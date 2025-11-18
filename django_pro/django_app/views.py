from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from .models import CloudTable
from .serializers import CloudTableSerializer
import json
import cloudinary
import cloudinary.uploader
import bcrypt
import jwt
import datetime
import re
from django.conf import settings
from django.core.mail import send_mail,EmailMessage
SECRET_KEY=settings.SECRET_KEY




# ------------------------ BASIC ROUTES ------------------------

def welcome(request):
    return HttpResponse("Welcome to Mani's app deployed on Render")


def sample(request):
    return JsonResponse({"msg": "JSON response from Render"})


# ------------------------ JWT VALIDATOR ------------------------

def is_valid_user(request):
    try:
        cookie_token = request.COOKIES.get("my_first_cookie")
        if not cookie_token:
            return False

        data = jwt.decode(jwt=cookie_token, key=SECRET_KEY, algorithms=["HS256"])
        return data      # return decoded payload

    except Exception:
        return False


# ------------------------ REGISTER USER ------------------------

@csrf_exempt
def reg_user(request):
    if request.method == "POST":
        try:
            user_name = request.POST.get("name")
            user_email = request.POST.get("email")
            user_mob = request.POST.get("mob")
            user_password = request.POST.get("password")
            user_image = request.FILES.get("profile")

            if not all([user_name, user_email, user_password]):
                return JsonResponse({"error": "name, email, and password are required"}, status=400)

            # Hash password
            encrypted_pass = bcrypt.hashpw(
                user_password.encode("utf-8"),
                bcrypt.gensalt(14)
            ).decode("utf-8")

            img_url = None
            if user_image:
                upload_result = cloudinary.uploader.upload(
                    user_image,
                    folder="user_profile_pic",
                    use_filename=True,
                    unique_filename=True,
                    overwrite=False
                )
                img_url = upload_result.get("secure_url")

            new_user = CloudTable.objects.create(
                email=user_email,
                name=user_name,
                mob=user_mob,
                profile_pic=img_url,
                password=encrypted_pass
            )

            serializer = CloudTableSerializer(new_user)
            send_mail(subject="welcome mail",
                      message="Welcome to the app!!",
                      recipient_list=[user_email],
                      from_email=settings.EMAIL_HOST_USER)
            return JsonResponse(
                {"msg": "User created successfully!", "user": serializer.data},
                status=201
            )

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Only POST method allowed"}, status=405)


# ------------------------ GET ALL USERS ------------------------

def get_users(request):
    if request.method == "GET":
        user = is_valid_user(request)

        if user and user.get("valid_user"):
            users = CloudTable.objects.all()
            serializer = CloudTableSerializer(users, many=True)
            return JsonResponse(serializer.data, safe=False)

        res = HttpResponse("invalid user")
        res.delete_cookie("my_first_cookie")
        return res

    return JsonResponse({"error": "Only GET method allowed"}, status=405)


# ------------------------ GET USER BY ID ------------------------

def get_user_by_id(request, id):
    if request.method == "GET":
        try:
            user = CloudTable.objects.get(id=id)
            serializer = CloudTableSerializer(user)
            return JsonResponse(serializer.data, safe=False)
        except CloudTable.DoesNotExist:
            return JsonResponse({"error": "User not found"}, status=404)

    return JsonResponse({"error": "Only GET method allowed"}, status=405)


# ------------------------ UPDATE USER ------------------------

@csrf_exempt
def update_user(request, id):
    if request.method == "PUT":
        try:
            user = CloudTable.objects.get(id=id)

            # Multipart or JSON
            if request.content_type.startswith("multipart/form-data"):
                data = request.POST
                new_image = request.FILES.get("profile")
            else:
                data = json.loads(request.body)
                new_image = None

            user.name = data.get("name", user.name)
            user.email = data.get("email", user.email)
            user.mob = data.get("mob", user.mob)

            # Password update
            new_password = data.get("password")
            if new_password:
                hashed_pass = bcrypt.hashpw(
                    new_password.encode("utf-8"),
                    bcrypt.gensalt(14)
                ).decode("utf-8")
                user.password = hashed_pass

            # Replace image
            if new_image:
                if user.profile_pic:
                    try:
                        match = re.search(r"user_profile_pic/([^\.]+)", user.profile_pic)
                        if match:
                            public_id = f"user_profile_pic/{match.group(1)}"
                            cloudinary.uploader.destroy(public_id)
                    except:
                        pass

                upload_result = cloudinary.uploader.upload(
                    new_image,
                    folder="user_profile_pic",
                    use_filename=True,
                    unique_filename=True,
                    overwrite=True
                )
                user.profile_pic = upload_result.get("secure_url")

            user.save()
            serializer = CloudTableSerializer(user)

            return JsonResponse(
                {"msg": "User updated successfully", "user": serializer.data},
                status=200
            )

        except CloudTable.DoesNotExist:
            return JsonResponse({"error": "User not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Only PUT method allowed"}, status=405)


# ------------------------ DELETE USER ------------------------

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


# ------------------------ LOGIN USER ------------------------

@csrf_exempt
def login_user(req):
    user_data = json.loads(req.body)

    try:
        user = CloudTable.objects.get(id=user_data["id"])
    except CloudTable.DoesNotExist:
        return HttpResponse("User not found", status=404)

    serialized = CloudTableSerializer(user).data

    encrypted_pass = serialized["password"]
    user_pass = user_data["password"]

    is_same = bcrypt.checkpw(user_pass.encode("utf-8"), encrypted_pass.encode("utf-8"))

    if not is_same:
        return HttpResponse("invalid credentials", status=401)

    # JWT payload
    payload = {
        "name": serialized["name"],
        "email": serialized["email"],
        "valid_user": True,
        "user_id": serialized["id"],
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30),
        "iat": datetime.datetime.utcnow()
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

    res = HttpResponse("cookie is set in the browser")
    res.set_cookie(
        key="my_first_cookie",
        value=token,
        httponly=True,       # JS cannot access
        max_age=1800         # 30 minutes
    )

    return res

@csrf_exempt
def send_file(req):
    user_email=req.POST.get("user")
    pic=req.POST.get("file")
    email=EmailMessage(
        subject="sending file",
        body='this is the file',
        from_email=settings.EMAIL_HOST_USER,
        to=[user_email]
    )
    email.attach_file("C:/Users/ravig/Pictures/Nitro/Nitro_Wallpaper_5000x2813.jpg")
    email.send()
    return HttpResponse("mail sent successfully!")




#documentation
  















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



# hashing

# database compromise

# login  
# username 
# password  -> hash -> store

# bcrypt
# gensalt-> 
# hashpw








# hashpw     -> hashed
# checkpw    -> hashed , user pass
# encode("utf-8")


# login 
# homepage



# about
# categories
# my account 
# contact



# local storage
# session storage





# session storage {"logged":true}


# tokens 
# entry token - qr  code  
                # token
# food token



#authentication-> identity   -> who u are
#authorization  -> what u can do



# employee

# dev
# test
# hr 
# manager 
# devops

# hash-> irreversible 
#  encoding ->reversible


# jwt -> encode  -> payload   key   algorithm-HS256   -> encoded string   
#     -> decode -> string     key   algorithm-256     -> payload



# login > jwt token with user details > copy the token and verify in JWT.io

















# token: piece of data  exchanged btw client and server
# -> generate token 

# JWT -> JSON web token 

# payload  data 
# key     security 
# algo    process

# jwt.encode(payload="",key="",algorithm="HS256")
# jwt.decode (token,key="",algorithms="HS256")


# server side -> token

# req->

# local 
# session

# cookie  ->



# cookies: is a type of storage to store tokens and other data

# why?
# it helps in two way communication from both  FE and BE


# create res 
# res.set_cookie(
#     key=name 
#     value=data,
#     httponly=True  # js cant access 
#     maxage=60  #life time of a cookie
# )
# return res



#cookies 

#type of storage 
# usedata
# is session active
# analysis



# res .
# res.set_cookie(
    
# )


# message

# otp
# TRAI - Telephone Regualtory Authority of India
# app -reg 
# protocols
# procedure
# persmissions



# email- smtp 
# Simple  Mail Transfer Protocol
# receipents mail 
# senders mail
# content 