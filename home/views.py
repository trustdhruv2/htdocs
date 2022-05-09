from django.shortcuts import render

from responsehandler.response import response
from .models import services as sdata


def home(request):
    print(request.user)
    return response(request.META["HTTP_USER_AGENT"]).response(request,"home.html","home.html")


def services(request):
    servicedata = {}
    data = sdata.objects.all()
    for i in data:
        servicedata[i.name] = [i.thumbnail, i.description]
    return response(request.META["HTTP_USER_AGENT"]).response(request,"services.html","services.html",{"services":servicedata})

def aboutus(request):
    return response(request.META["HTTP_USER_AGENT"]).response(request,"about.html","about.html")

def contactus(request):
    return response(request.META["HTTP_USER_AGENT"]).response(request,"contactus.html","contactus.html")
def pricing(request):
    return response(request.META["HTTP_USER_AGENT"]).response(request,"pricing.html","pricing.html")
