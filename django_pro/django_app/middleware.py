# from django.http import HttpResponse




# class SampleMiddleware:
#     ## initiate once when the server is started
#     def __init__(self,get_response):
#         self.get_response=get_response
#         print("initiated once")

#     ## it is executed for every request
#     def __call__(self, request):
#         print("before the request from sample middleware")
#         response=self.get_response(request)
#         print("after the request")
#         # return HttpResponse("i will not allow!")
#         return response

# class LastMiddleware:
#     def __init__(self,get_response) :
#         self.get_response=get_response
#         print("last middleware initiated ")
    

#     def __call__(self,request):
#         print("before last from last middleware")

#         #exceptions 
#         #try except  else finally 
#         try:
#              cookie=request.COOKIES.get("sample")
            
#              print(type(cookie),"cookie",dir(request))
#              request.COOKIES["name"]="manivardhan"
#              print(request,"from the if condition")
#              response=self.get_response(request)
#              return response
#         except:
#             return  HttpResponse("invalid request!!") 


        




# ## __init__

# ## __call__