from django.db import models
from course.models import courses
from course.models import coursecategory
from django.contrib.auth.models import User
from datetime import datetime


class enrollments(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    course = models.ForeignKey(to=courses, on_delete=models.CASCADE, default=None)
    enrolledon = models.DateTimeField(default=datetime.now())
    completedon = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.user.username


class domainenrollment(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    domain = models.ForeignKey(to=coursecategory, on_delete=models.CASCADE, default=None)
    enrolledon = models.DateTimeField(default=datetime.now())
    expiry = models.DateTimeField()

    def __str__(self):
        return self.user.username
