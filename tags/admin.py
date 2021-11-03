from django.contrib import admin
from django.db import models
from tags.models import Tag,TggedItems

# Register your models here.
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    search_fields=['label']

admin.site.register(TggedItems)