from django.db import models

class queries(models.Model):
    name=models.TextField()
    email=models.EmailField()
    phone=models.CharField(max_length=10)
    organization=models.TextField(null=True)
    subject=models.TextField()
    message=models.TextField()
    status=models.BooleanField()
    def __str__(self):
        return self.message