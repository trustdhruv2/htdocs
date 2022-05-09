from django.contrib import admin

from queries.models import queries

@admin.register(queries)
class PersonAdmin(admin.ModelAdmin):
    list_display = ("name", "subject","message","status")