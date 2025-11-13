from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .models import CloudTable
from .serializers import CloudTableSerializer
import json
import cloudinary
import bcrypt
import re
import jwt
import datetime
from django.conf import settings  
SECRETKEY = settings.SECRET_KEY  


def welcome(request):

    return HttpResponse("Welcome to Mani's app deployed on Render ")


def sample(request):
    return JsonResponse({"msg": "JSON response from Render"})




@csrf_exempt
def reg_user(request):
    if request.method == "POST":
        try: 
            user_name = request.POST.get("name")
            user_email = request.POST.get("email")
            user_mob = request.POST.get("mob")
            user_password = request.POST.get("password")
            user_image = request.FILES.get("profile")

            # ✅ Basic validation
            if not all([user_name, user_email, user_password]):
                return JsonResponse({"error": "name, email, and password are required"}, status=400)

            # ✅ Password hashing
            user_password = user_password.encode("utf-8")
            u_salt = bcrypt.gensalt(rounds=14)
            encrypted_pass = bcrypt.hashpw(password=user_password, salt=u_salt).decode("utf-8")

            # ✅ Upload image to Cloudinary inside users_folder/
            img_url = None
            if user_image:
                upload_result = cloudinary.uploader.upload(
                    user_image,
                    folder="user_profile_pic",  # 👈 All images go here
                    use_filename=True,      # keeps original filename
                    unique_filename=True,   # adds unique ID if name repeats
                    overwrite=False
                )
                img_url = upload_result.get("secure_url")

            # ✅ Create user (AutoField id)
            new_user = CloudTable.objects.create(
                email=user_email,
                name=user_name,
                mob=user_mob,
                profile_pic=img_url,
                password=encrypted_pass
            )

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

            # Check if content type is multipart (for files) or JSON
            if request.content_type.startswith("multipart/form-data"):
                data = request.POST
                new_image = request.FILES.get("profile")
            else:
                data = json.loads(request.body)
                new_image = None

            # ✅ Update basic fields
            user.name = data.get("name", user.name)
            user.email = data.get("email", user.email)
            user.mob = data.get("mob", user.mob)

            # ✅ Update password (hash it again if provided)
            new_password = data.get("password")
            if new_password:
                hashed_pass = bcrypt.hashpw(new_password.encode("utf-8"), bcrypt.gensalt(14)).decode("utf-8")
                user.password = hashed_pass

            # ✅ Replace image: delete old one and upload new
            if new_image:
                # If user already has an image, delete it from Cloudinary
                if user.profile_pic:
                    try:
                        # Extract public_id from the URL using regex
                        match = re.search(r"user_profile_pic/([^\.]+)", user.profile_pic)
                        if match:
                            public_id = f"user_profile_pic/{match.group(1)}"
                            cloudinary.uploader.destroy(public_id)
                    except Exception as e:
                        print("Warning: Failed to delete old image:", str(e))

                # Upload new image
                upload_result = cloudinary.uploader.upload(
                    new_image,
                    folder="users_folder",
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




def login_user(req):
    user_data=json.loads(req.body)
    user=CloudTable.objects.get(id=user_data["id"])
    serialized_Data=CloudTableSerializer(user)
    # print(serialized_Data.data)
    encrypted_pass=serialized_Data.data["password"]
    user_pass=user_data["password"]
    is_same=bcrypt.checkpw(user_pass.encode("utf-8"),encrypted_pass.encode("utf-8"))


    ##creating jwt 
    user_payload={
        "name":serialized_Data.data["name"],
        "email":serialized_Data.data["email"],
        # "name":"jhonny",
        # "email":"pavan@dcm.com",
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30),
        "iat": datetime.datetime.utcnow()
    }

    token=jwt.encode(payload=user_payload,key=SECRETKEY,algorithm="HS256")
    # print(token)
    if is_same:
     res=HttpResponse("cookie is set in the browser")
     res.set_cookie(
            key="my_first_cookie",  # cookie name
            value=token, ## what data to be stored (string)
            httponly=True, ## to allow js to access the cookie
            max_age=3  ## till when the cookie is valid
        )
     return res

    else:
        return HttpResponse("invalid credentials")
  















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