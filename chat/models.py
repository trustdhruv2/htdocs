from django.db import models
from django.contrib.auth.models import User
from course.models import coursecategory
from enroll.models import domainenrollment


class ChatChannel(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    channel = models.TextField()

    def __str__(self):
        return self.channel


class Chats(models.Model):
    sender = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="sender")
    receiver = models.ForeignKey(to=User, on_delete=models.CASCADE,related_name="receiver")
    message = models.TextField()
    instance = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.sender.username


class Instructor(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    domain = models.ForeignKey(to=coursecategory, on_delete=models.CASCADE)
    experience = models.PositiveIntegerField()

    def __str__(self):
        return self.user.username
