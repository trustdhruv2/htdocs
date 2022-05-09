from django.shortcuts import redirect

from responsehandler.response import response
from .enrolled import enrolled


def dashboard(request):
    courses = enrolled().getenrollments(request.user)
    if courses == -1:
        return redirect("/login")
    else:
        edata = []
        for i in courses:
            isenrolled = lambda: True if enrolled().categoryenrolled(request.user, i.course.course) else False
            edata.append({"course": i, "enrolled": isenrolled()})
        return response(request.META["HTTP_USER_AGENT"]).response(request, "dashboard.html", "dashboard-mobile.html", {"courses": edata})
