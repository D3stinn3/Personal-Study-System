from django.contrib import admin

# Register your models here.

from .models import Document, Subject

admin.site.register(Document)
admin.site.register(Subject)