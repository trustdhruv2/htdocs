from django.contrib.auth.models import User
from django.db import models


class coursecategory(models.Model):
    choose = {"1": "Beginner", "2":"Intermediate", "3": "Advanced"}
    name = models.CharField(max_length=40)
    thumbnail = models.URLField()
    rating = models.PositiveSmallIntegerField()
    level = models.CharField(max_length=30, choices=[("1", "Beginner"), ("2", "Intermediate"), ("3", "Advanced")])
    description = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Course category"


class courses(models.Model):
    choose = {"1": "Beginner", "2": "Intermediate", "3": "Advanced"}
    course = models.ForeignKey(to=coursecategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=40)
    thumbnail = models.URLField()
    rating = models.PositiveIntegerField()
    level = models.CharField(max_length=30, choices=[("1", "Beginner"), ("2", "Intermediate"), ("3", "Advanced")])
    description = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Courses"


class courseskills(models.Model):
    course = models.ForeignKey(to=courses, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Skills required"


class module(models.Model):
    course = models.ForeignKey(to=courses, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Modules"


class userprogress(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    module = models.ForeignKey(to=module, on_delete=models.CASCADE)
    status = models.SmallIntegerField(default=2)

    def __str__(self):
        return self.module.name

    class Meta:
        verbose_name_plural = "Progress"


class questionnaire(models.Model):
    module = models.ForeignKey(to=module, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    questions = models.PositiveIntegerField(default=10)
    max_attempts = models.PositiveIntegerField(default=5)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Questionnaire"


class questionbank(models.Model):
    questionnaire = models.ForeignKey(to=questionnaire, on_delete=models.CASCADE)
    question = models.TextField()
    A = models.TextField()
    B = models.TextField()
    C = models.TextField()
    D = models.TextField()
    correct = models.CharField(max_length=1, choices=[("A", "A"), ("B", "B"), ("C", "C"), ("D", "D")])
    explanation = models.TextField()

    def __str__(self):
        return self.questionnaire.name

    class Meta:
        verbose_name_plural = "Question bank"


class lecture(models.Model):
    module = models.ForeignKey(to=module, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    source = models.URLField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Lectures"


class scoreboard(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    assignment = models.ForeignKey(to=questionnaire, on_delete=models.CASCADE)
    score = models.PositiveIntegerField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class assignmentboard(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    assignment = models.ForeignKey(to=questionnaire, on_delete=models.CASCADE)
    attempt = models.PositiveIntegerField(default=1)
    question = models.ForeignKey(to=questionbank, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class usersolutionboard(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    assignment = models.ForeignKey(to=assignmentboard, on_delete=models.CASCADE)
    solution = models.CharField(max_length=1, choices=[("A", "A"), ("B", "B"), ("C", "C"), ("D", "D")])

    def __str__(self):
        return self.user.username

