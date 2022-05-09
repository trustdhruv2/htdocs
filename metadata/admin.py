from django.contrib import admin

# Register your models here.
from metadata.models import dcsinfo, subscription

admin.site.register(dcsinfo)
admin.site.register(subscription)
