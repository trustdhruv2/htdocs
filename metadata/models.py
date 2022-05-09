from django.db import models
from account.models import states
from course.models import *
# Create your models here.


class dcsinfo(models.Model):
    name = models.CharField(max_length=30)
    state = models.ForeignKey(to=states, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class subscription(models.Model):
    course = models.ForeignKey(to=coursecategory, on_delete=models.CASCADE)
    duration = models.PositiveIntegerField()
    price = models.PositiveIntegerField()

    def __str__(self):
        return self.course.name
