from django.core.checks import messages
from django.db import models
from django.http.response import HttpResponse
from queries.models import queries

def addquery(request):
    if(request.method=="POST"):
        if(request.POST.get("company",None)==None):
            queries.objects.create(name=request.POST["name"],email=request.POST["email"],subject=request.POST["subject"],phone=request.POST["phone"],message=request.POST["message"],status=False)
        else:
            queries.objects.create(name=request.POST["name"],organization=request.POST["company"],email=request.POST["email"],subject=request.POST["subject"],phone=request.POST["phone"],message=request.POST["message"],status=False)
    return HttpResponse("OK")