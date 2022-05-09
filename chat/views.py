import json

from asgiref.sync import async_to_sync
from channels import DEFAULT_CHANNEL_LAYER
from channels.layers import get_channel_layer
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect,render
from django.views.decorators.csrf import csrf_exempt

from chat.models import Instructor, ChatChannel, Chats
from enroll.models import domainenrollment
from responsehandler.response import response


def closeallchannels(request):
    if not request.user.is_anonymous:
        channels = ChatChannel.objects.filter(user=User.objects.get(id=request.user.id))
        layer = get_channel_layer(alias=DEFAULT_CHANNEL_LAYER)
        for i in channels:
            i.delete()
            chan=i.channel
            async_to_sync(layer.send)(chan, {
                "type": "forceremove",
            })
    else:
        return redirect("/login")
    return redirect("/instructorchat")


def chathandler(request):
    if request.user.is_anonymous:
        return redirect("/login")
    else:
        return response(request.META["HTTP_USER_AGENT"]).response(request, "instructorchat.html", "instructorchat-mobile.html")


def getchannels(request):
    channels = []
    if not request.user.is_staff:
        domains = domainenrollment.objects.filter(user=request.user)
        for i in domains:
            instructors = Instructor.objects.filter(domain=i.domain)
            for j in instructors:
                try:
                    ChatChannel.objects.get(user=j.user)
                    channels.append({"member": {"username": j.user.username, "id": j.user.id}, "active": 1})
                except ObjectDoesNotExist:
                    channels.append({"member": {"username": j.user.username, "id": j.user.id}, "active": 0})
        return JsonResponse({"code": 200, "data": channels})
    else:
        try:
            enrollments = domainenrollment.objects.filter(domain=Instructor.objects.get(user=request.user).domain).exclude(user=request.user)
            for j in enrollments:
                try:
                    ChatChannel.objects.get(user=j.user)
                    channels.append({"member": {"username": j.user.username, "id": j.user.id}, "active": 1})
                except ObjectDoesNotExist:
                    channels.append({"member":  {"username": j.user.username, "id": j.user.id}, "active": 0})
            return JsonResponse({"code": 200, "data": channels})
        except ObjectDoesNotExist:
            return JsonResponse({"code": 400})


@csrf_exempt
def getchats(request):
    if request.method == "POST":
        freind = User.objects.get(id=request.POST.get("id", None))
        chats = Chats.objects.filter(Q(sender=request.user, receiver=freind) | Q(receiver=request.user, sender=freind)).order_by("instance")
        active = (len(ChatChannel.objects.filter(user=freind)) > 0)
        messagedata = {"username": freind.username, "active": active}
        msg = []
        for i in chats:
            msg.append({"str": i.sender.id == request.user.id, "message": i.message, "instance": i.instance.strftime('%H:%M:%S')})
        messagedata["msg"] = msg
        return JsonResponse(json.dumps(messagedata), safe=False)
    else:
        return HttpResponse("404")
