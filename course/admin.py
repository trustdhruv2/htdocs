from django.contrib import admin

from course.models import *

# Register your models here.

admin.site.register(coursecategory)

admin.site.register(courses)

admin.site.register(module)

admin.site.register(scoreboard)

admin.site.register(usersolutionboard)

admin.site.register(userprogress)

admin.site.register(assignmentboard)

admin.site.register(lecture)

admin.site.register(questionnaire)

admin.site.register(courseskills)

admin.site.register(questionbank)
