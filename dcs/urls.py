from django.contrib import admin
from django.urls import path


from course.views import *
from account.views import loginview, sos, logoutview, register, verifyuser, getschools, mailverify, registeruser, account, updatepublic, changepassword, changeemail, storenewmail, changephone
from chat.views import chathandler, closeallchannels, getchats, getchannels
from enroll.views import dashboard
from home.views import aboutus, contactus, home, pricing, services
from course.views import domains, courselist, description
from chat.chat_frame import Channel
from privacy.views import privacy
from queries.views import addquery

urlpatterns = [
    path('admin/', admin.site.urls),
    path('services', services),
    path('category', domains),
    path('courses', courselist),
    path('description', description),
    path('dashboard', dashboard),
    path('instructorchat', chathandler),
    path('uhere', closeallchannels),
    path('getchannels', getchannels),
    path('getchats', getchats),
    path('mailverify', mailverify),
    path('sos', sos),
    path('getcontent', getlectures),
    path('validator', validateassignment),
    path('getschools', getschools),
    path('verifyuser', verifyuser),
    path('getassignment', getassignment),
    path('register', register),
    path('login', loginview),
    path("enroll", enroller),
    path("account", account),
    path("changepassword", changepassword),
    path("updatepublic", updatepublic),
    path("changeemail", changeemail),
    path("storenewmail", storenewmail),
    path('changephone', changephone),
    path("logout", logoutview),
    path('registeruser', registeruser),
    path('courseindex', courseindex),
    path('about', aboutus),
    path('privacy', privacy),
    path('addquery', addquery),
    path('pricing', pricing),
    path('contact', contactus),
    path('lectures', lectures),
    path('', home)
]
channel_urls = [
    path('chat', Channel.as_asgi()),
]
