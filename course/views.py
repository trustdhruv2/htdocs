import json
import random
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect

from account.models import other_details
from course.models import *
from metadata.models import dcsinfo, subscription
from responsehandler.response import response
from enroll.models import *
from enroll.enrolled import *


def getlecture(lectures, lid):
    i, j = 0, len(lectures)-1
    key = int(lid)
    while i <= j:
        mid = int((i+j)/2)
        if lectures[mid].id == key:
            return lectures[mid]
        if key < mid:
            j = mid-1
        else:
            i = mid+1
    return None


def getassignment(request):
    if request.user.is_anonymous:
        return JsonResponse({"error": "-2"})
    assignment = questionnaire.objects.get(id=request.POST.get("aid", None))
    if not enrolled().isenrolled(request.user, assignment.module.course):
        return JsonResponse({"error": "-3"})
    c_attempt = len(scoreboard.objects.filter(user=request.user, assignment=assignment))+1
    questions = assignmentboard.objects.filter(user=request.user, assignment=assignment, attempt=c_attempt)
    if len(questions) == 0:
        qbank = generate_assignment(assignment)
        for i in qbank:
            assignmentboard.objects.create(user=request.user, assignment=assignment, attempt=c_attempt, question=questionbank.objects.get(id=i))
        request.session["assignment"] = {"id": assignment.id}
        return JsonResponse({"assignment": qbank})
    assignment = {}
    for i in questions:
        i = i.question
        assignment[i.id] = [i.question, i.A, i.B, i.C, i.D]
    return JsonResponse({"assignment": assignment})


def generate_assignment(assignment):
    bank = questionbank.objects.filter(questionnaire=assignment)
    y_limit = assignment.questions
    result = {}
    if len(bank) == 0:
        return result
    i = random.randrange(0, len(bank))
    limit = 0
    if len(bank) > y_limit:
        limit = 10
    else:
        limit = len(bank)
    while len(result) != limit:
        if bank[i].id not in result.keys():
            result[bank[i].id] = [bank[i].question, bank[i].A, bank[i].B, bank[i].C, bank[i].D]
        i = random.randrange(0, len(bank))
    return result


def validateassignment(request):
    if request.user.is_anonymous:
        return JsonResponse({"error": "-2"})
    if not request.session["assignment"]:
        return JsonResponse({"error": "-3"})
    useranswers = json.loads(request.POST.get("paper", None))
    assignment = request.session["assignment"]
    del request.session["assignment"]
    questions = assignmentboard.objects.filter(user=request.user, assignment=questionnaire.objects.get(id=assignment["id"]),attempt=len(scoreboard.objects.filter(user=request.user, assignment=questionnaire.objects.get(id=assignment["id"])))+1)
    if len(useranswers.keys()) != len(questions):
        return JsonResponse({"error": "-4"})
    score = len(questions)
    incorrect = 0
    for i in questions:
        if useranswers[str(i.question.id)] != i.question.correct:
            score -= 1
            incorrect += 1
        usersolutionboard.objects.create(user=request.user, assignment=i,solution=useranswers[str(i.question.id)])
    score = (score/len(questions))*100
    id = scoreboard.objects.create(user=request.user, assignment=questionnaire.objects.get(id=assignment["id"]), score=score).id
    return JsonResponse({"id": id, "score": score, "incorrect": incorrect, "correct": len(questions)-incorrect})


def getlectures(request):
    try:
        if request.user.is_anonymous:
            return JsonResponse({"error": -1})
        lectures = lecture.objects.filter(module=userprogress.objects.get(user=request.user, module=module.objects.get(id=request.GET.get("mid", None)), status=2).module)
        assignment = questionnaire.objects.get(module=userprogress.objects.get(user=request.user, module=module.objects.get(id=request.GET.get("mid", None))).module)
        yscore = scoreboard.objects.filter(user=request.user, assignment=assignment).order_by("-date")
        content = []
        scores = []
        for i in lectures:
            content.append({"id": i.id, "name": i.name, "url": i.source})
        for i in range(0, min(len(yscore), 5)):
            n = len(assignmentboard.objects.filter(user=request.user, assignment=yscore[i].assignment, attempt=i+1))
            correct = (yscore[i].score/100)*n
            incorrect = n-correct
            scores.append({"id": yscore[i].id, "score": yscore[i].score, "date": yscore[i].date,"questions": n,"correct": correct,"incorrect": incorrect})
        return JsonResponse({"lectures": content, "assignment": {"id": assignment.id, "name": assignment.name, "questions": assignment.questions, "attempts allowed": assignment.max_attempts}, "scores": scores})
    except ObjectDoesNotExist:
        try:
            md = module.objects.get(id=request.GET.get("mid", None))
            if not enrolled().isenrolled(request.user, md.course):
                return JsonResponse({"error": -2})
            else:
                return JsonResponse({"error": -3})
        except ObjectDoesNotExist:
            return JsonResponse({"error": -4})


def lectures(request):
    if request.user.is_anonymous:
        return redirect("/login")
    c = module.objects.get(id=request.GET.get("mid", None)).course.course
    if not enrolled().categoryenrolled(request.user, c):
        return redirect("/enroll?eid="+str(c.id))
    return response(request.META["HTTP_USER_AGENT"]).response(request, "lectures.html", "lectures-mobile.html")


def courseindex(request):
    try:
        if request.user.is_anonymous:
            return redirect("/login")
        c = courses.objects.get(id=request.GET.get("cid",None))
        if not enrolled().categoryenrolled(request.user, c.course):
            return redirect("/enroll?eid="+str(c.id))
        data = module.objects.filter(course=enrollments.objects.get(user=request.user, course=c).course)
        progress = userprogress.objects.filter(user=request.user)
        status = {}
        i, j = 0, 0
        eligible = True
        while i < len(data) and j < len(progress):
            if data[i].name not in status.keys():
                status[data[i].name] = {"status": 3, "id": data[i].id}
            if progress[j].status == 3 or progress[j].status == 2:
                eligible = False
            status[progress[j].module.name] = {"status": progress[j].status, "id": progress[j].module.id}
            i += 1
            j += 1
        while i < len(data):
            if data[i].name not in status.keys():
                eligible = False
                status[data[i].name] = {"status": 3, "id": data[i].id}
            i += 1
        return response(request.META["HTTP_USER_AGENT"]).response(request, "courseindex.html", "courseindex-mobile.html",{"course":c,"modules":status,"eligible":eligible})
    except ObjectDoesNotExist:
        return HttpResponse("404")


def domains(request):
    name = request.GET.get("name")
    level = request.GET.get("level")
    p1 = request.GET.get("p1")
    p2 = request.GET.get("p2")
    result = []
    if name is not None and level is not None and p1 is not None and p2 is not None:
        rs = coursecategory.objects.filter(name=name, level=level)
        for i in range(0, len(rs)):
            subs = subscription.objects.filter(course=rs[i]).order_by("duration")
            if len(subs) > 0 and subs[0].price in range(p1, p2):
                result.append(subs[0])
    else:
        rs = coursecategory.objects.all()
        for i in range(0, len(rs)):
            subs = subscription.objects.filter(course=rs[i]).order_by("duration")
            if len(subs) > 0:
                result.append(subs[0])
                
    category = []
    thumbnail = []
    difficulty = []
    price1 = []
    domains = []
    enrollments = set()
    x = enrolled().categoryenrollments(request.user)
    if x != -1:
        for i in x:
            enrollments.add(i.domain.id)
    for j in result:
        domains.append({"domain": j, "enrolled": j.course.id in enrollments})
        difficulty.append(j.course.level)
        price1.append(j.price)
        thumbnail.append(j.course.thumbnail)
        category.append(j.course.name)
        price1 = list(set(price1))
    
    return response(request.META["HTTP_USER_AGENT"]).response(request, "courses.html", "courses-mobile.html", {"coursedata": domains, "category": set(category), "difficulty": set(difficulty), "p1": price1, "choose":courses.choose})


def courselist(request):
    try:
        cid = request.GET.get("cid")
        name = request.GET.get("name")
        level = request.GET.get("level")
        rating = request.GET.get("rating")
        enrollments = enrolled().getenrollments(request.user)
        ccategory = coursecategory.objects.get(id=cid)
        if name is not None and level is not None and rating is not None:
            clist = courses.objects.filter(course=ccategory,name=name,level=level,rating=rating)
        else:
            clist = courses.objects.filter(course=ccategory)
    except:
        clist = []
    fname = set()
    levels = set()
    rating = set()
    for i in clist:
        fname.add(i.name)
        levels.add(i.level)
        rating.add(i.rating)
    rating = list(rating)
    rating.sort(reverse=True)
    return response(request.META["HTTP_USER_AGENT"]).response(request, "clist.html", "clist-mobile.html", {"clist": clist, "name":fname,"levels":levels,"choose":courses.choose,"rating":rating, "enrollments": enrollments})


def description(request):
    if request.method == "POST":
        if not request.user.is_anonymous:
            pid = request.POST.get("pid")
            course = courses.objects.get(id=pid)
            if enrolled().categoryenrolled(request.user, course.course):
                m = module.objects.filter(course=course)
                if len(m) > 0:
                    enrollments.objects.create(user=request.user, course=course)
                    userprogress.objects.create(user=request.user, module=m[0])
                    return redirect("/dashboard")
                else:
                    return HttpResponse("course is under development")
            else:
                return redirect("/enroll?eid="+str(course.course.id))
        else:
            return redirect("/login")
    pid = request.GET.get("pid")
    course = courses.objects.get(id=pid)
    eobj = enrolled()
    isenrolled = eobj.isenrolled(request.user, course)
    modules = module.objects.filter(course=course)
    skills = courseskills.objects.filter(course=course)
    content = {}
    lectures = 0
    llq = 0
    llist=[]
    for i in modules:
        llist = lecture.objects.filter(module=i)
        lq = questionnaire.objects.filter(module=i)
        llq += len(lq)
        lectures += len(llist)
        content[i.name] = [llist, lq]
    return response(request.META["HTTP_USER_AGENT"]).response(request, "description.html", "description-mobile.html", {"product": course, "choose": courses.choose, "skills": skills, "content": content, "lectures": llist, "assignment": llq, "llist": lectures, "isenrolled": isenrolled})


def enroller(request):
    if request.user.is_anonymous:
        return redirect("/login")
    if request.method == "POST":
        return redirect("/enroll?eid="+request.POST.get("eid"))
    sid = request.GET.get("sub", -1)
    cc = coursecategory.objects.get(id=request.GET.get("eid", None))
    sub = subscription.objects.filter(course=cc).order_by("duration")
    if len(sub) == 0:
        return HttpResponse("404")
    subs = []
    subamount = 0
    for i in sub:
        if int(sid) == i.id:
            subamount += i.price
        subs.append({"id": i.id, "price": i.price, "duration": i.duration, "default": int(sid) == i.id})
    if sid == -1:
        subamount += subs[0]["price"]
        subs[0]["default"] = True
    discount = 0
    price = (subamount-discount)+(0.18*subamount)
    fromsame = dcsinfo.objects.all()[0].state == other_details.objects.get(user=request.user).state
    return response(request.META["HTTP_USER_AGENT"]).response(request, "enroll.html", "enroll-mobile.html", {"subs": subs,"product": cc, "subamount": subamount, "price": price, "fromsame": fromsame, "discount": discount})
