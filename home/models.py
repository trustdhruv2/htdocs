from django.db import models

# Create your models here.
class services(models.Model):
    name = models.CharField(max_length=40)
    thumbnail=models.URLField()
    description=models.TextField()
    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Services"