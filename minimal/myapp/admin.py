from django.apps import apps
from django.contrib import admin
from .models import Document

class DocumentAdmin(admin.ModelAdmin):
    list_display  = ('docfile', 'uploaded', 'is_special')
admin.site.register(Document, DocumentAdmin)

