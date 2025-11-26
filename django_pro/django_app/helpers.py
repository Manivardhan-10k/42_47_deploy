##helper functions  


from django.http import HttpResponse


def sample_decorator(func):   ## func is the view on which decorator is applied
    print("before the function")
    def wrapper(request,*args,**kwargs): ## for performing validations
        if request.COOKIES.get("sample"):
          return  func(request)
        else:
           return HttpResponse("cookie must be present ")
    return wrapper