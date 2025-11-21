from django.http import HttpResponse



class LastMiddleware:
    def __init__(self,get_response) :
        self.get_response=get_response
        print("last middleware initiated ")
    

    def __call__(self,request):
        print("before last")
        response=self.get_response(request)

        return response
class SampleMiddleware:
    ## initiate once when the server is started
    def __init__(self,get_response):
        self.get_response=get_response
        print("initiated once")

    ## it is executed for every request
    def __call__(self, request):
        print("before the request")
        response=self.get_response(request)
        print("after the request")
        # return HttpResponse("i will not allow!")
        return response

        




## __init__

## __call__