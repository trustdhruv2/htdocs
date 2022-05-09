from django.contrib.auth.models import User
from django.db import models


class states(models.Model):
    state = models.CharField(max_length=30)

    def __str__(self):
        return self.state


class contacts(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    contact = models.CharField(max_length=13)

    def __str__(self):
        return self.contact

    class Meta:
        verbose_name_plural = "Active contacts"


class other_details(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    gender = models.SmallIntegerField(choices=[(0, "Male"), (1, "Female"), (2, "Other")])
    state = models.ForeignKey(to=states, on_delete=models.CASCADE)
    address = models.TextField()
    active_contact = models.ForeignKey(to=contacts, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = "Other details"


class school(models.Model):
    name = models.CharField(max_length=70)
    location = models.TextField()
    joined_on = models.DateField()
    active = models.BooleanField()

    def __str__(self):
        return self.name


class student(models.Model):
    user = models.ForeignKey(to=other_details, on_delete=models.CASCADE)
    school = models.ForeignKey(to=school, on_delete=models.CASCADE)