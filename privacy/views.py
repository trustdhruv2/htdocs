from django.shortcuts import render

from responsehandler.response import response

# Create your views here.
def privacy(request):
    return  response(request.META["HTTP_USER_AGENT"]).response(request,"privacy.html","privacy.html")
    