
# Create your views here.
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse
from django.shortcuts import redirect
from django.core.exceptions import ObjectDoesNotExist,MultipleObjectsReturned

from account.models import school, other_details, contacts, student, states
from enroll.models import enrollments, domainenrollment
from responsehandler.response import response
import pyrebase
from dcs.settings import firebaseConfig

options = {"profile": "1", "account settings": "2", "change password": "3", "billing": "4", "enrollments": "5"}


def mailverify(request):
    if request.session["rdata"]:
        return response(request.META["HTTP_USER_AGENT"]).response(request, "verifymail.html", "verifymail-mobile.html")
    else:
        return redirect("/register")


def changeemail(request):
    if request.user.is_anonymous:
        return redirect("/login")
    if request.method == "GET":
        return response(request.META["HTTP_USER_AGENT"]).response(request, "mailchange.html", "mailchange.html")
    request.user.email = request.session["nemail"]
    request.user.save()
    return redirect("/logout")


def changephone(request):
    if request.user.is_anonymous:
        return redirect("/login")
    if request.method == "GET":
        return None
    c = contacts.objects.filter(user=request.user)
    if len(c) == 0:
        c = contacts.objects.create(user=request.user, contact=request.POST.get("phone", None))
    else:
        c = c[0]
    user = other_details.objects.get(user=request.user)
    user.active_contact = c
    user.save()
    return redirect("/logout")


def changepassword(request):
    if request.user.is_anonymous:
        return redirect("/login")
    if request.method == "GET":
        return JsonResponse({"status":0})
    if authenticate(username=request.user.username, password=request.POST.get("old",None)) is not None:
        request.user.set_password(request.POST.get("new", None))
        return JsonResponse({"status":1})
    return JsonResponse({"status":2})


def updatepublic(request):
    if request.user.is_anonymous:
        return redirect("/login")
    if request.method == "GET":
        return None
    uobj = User.objects.filter(username=request.POST.get("username", None))
    others = other_details.objects.get(user=request.user)
    data = {"opt": "1", "udetails": others, "state": states.objects.all(),
            "option": options}
    if len(uobj) > 0 and uobj[0].username != request.user.username:
        data["invaliduname"] = True
        return response(request.META["HTTP_USER_AGENT"]).response(request, "account.html", "account-mobile.html", data)
    else:
        request.user.username = request.POST.get("username", None)
        others.state = states.objects.get(id=int(request.POST.get("state", None)))
        others.address = request.POST.get("address", None)
        others.gender = request.POST.get("gender", None)
        request.user.save()
        others.save()
        data["invaliduname"] = False
        return redirect("/account")


def storenewmail(request):
    if request.user.is_anonymous:
        return JsonResponse({"status": 0})
    request.session["nemail"] = request.GET.get("nemail")
    return JsonResponse({"status": 1})


def account(request):
    if request.user.is_anonymous:
        return redirect("/login")
    data = {}
    data = {"udetails": other_details.objects.get(user=request.user), "state": states.objects.all()}
    return response(request.META["HTTP_USER_AGENT"]).response(request, "account.html", "account-mobile.html", data)


def registeruser(request):
    if request.method == "POST":
        user = User.objects.create_user(request.session["rdata"]["username"], request.session["rdata"]["email"], request.session["rdata"]["password"])
        other_details.objects.create(user=user, gender=request.session["rdata"]["gender"], state=states.objects.get(id=request.session["rdata"]["state"]), address=request.session["rdata"]["address"], active_contact=contacts.objects.create(user=user, contact=request.session["rdata"]["contact"]))
        if str(request.session["rdata"]["mode"]) == "1":
            student.objects.create(user=user, school=school.objects.get(id=request.session["rdata"]["school"]))
        return JsonResponse({"code": 200})
    return JsonResponse({"code": 400})


def loginview(request):
    if request.method == "POST":
        try:
            user = authenticate(username=request.POST.get("username"), password=request.POST.get("password"))
            if user is not None:
                login(request, user)
                return redirect("/")
            else:
                return response(request.META["HTTP_USER_AGENT"]).response(request, "login.html", "login-mobile.html", {"invalid": 1})
        except ObjectDoesNotExist:
            return response(request.META["HTTP_USER_AGENT"]).response(request, "login.html", "login-mobile.html",
                                                                      {"invalid": 1})
    return response(request.META["HTTP_USER_AGENT"]).response(request, "login.html", "login-mobile.html")


def logoutview(request):
    if not request.user.is_anonymous:
        logout(request)
    return redirect("/")


def register(request):
    return response(request.META["HTTP_USER_AGENT"]).response(request, "registerp1.html", "registerp1-mobile.html")


def validator(data):
    return not(data["email"].isspace() or data["username"].isspace() or data["password"].isspace() or data["rpassword"].isspace() or data["gender"].isspace() or data["contact"].isspace())


def getschools(request):
    schools = school.objects.all()
    state = states.objects.all()
    schooljsondata=[]
    statejsondata=[]
    for i in schools:
        schooljsondata.append({"value": i.id, "text": i.name})
    for i in state:
        statejsondata.append({"value": i.id, "text": i.state})
    return JsonResponse({"code": 200, "schools": schooljsondata, "states": statejsondata})


def verifyuser(request):
    if request.method == "POST" and validator(request.POST):
        uobjs = User.objects.filter(email=request.POST["email"])
        if len(uobjs) == 0:
            uobjs = User.objects.filter(username=request.POST["username"])
            if len(uobjs) == 0:
                uobjs = contacts.objects.filter(contact=request.POST["contact"])
                if len(uobjs) == 0:
                    request.session["rdata"] = request.POST
                    return JsonResponse({"code": 200, "email": request.POST.get("email", None)})
                else:
                    return JsonResponse({"code": 370})
            else:
                return JsonResponse({"code": 350})
        else:
            return JsonResponse({"code": 300})
    else:
        return JsonResponse({"code": 400})


def sos(request):
    try:
        fapp = pyrebase.initialize_app(firebaseConfig)
        auth = fapp.auth()
        data = auth.get_account_info(request.GET.get("utoken", None))
        if data is not None:
            login(request, User.objects.get(email=data["users"][0]["email"]))
            return JsonResponse({"code": 1})
        else:
            return JsonResponse({"code": 2})
    except ObjectDoesNotExist:
        return JsonResponse({"code": 0})
    except Exception:
        return JsonResponse({"code": 500})