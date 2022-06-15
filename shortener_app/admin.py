from django.contrib import admin

from .models import UrlSaveModel


# Register your models here.
@admin.register(UrlSaveModel)
class UrlSaveModelAdmin(admin.ModelAdmin):
    list_display = ['key', 'created']
    readonly_fields = ['key', 'url', 'created', 'modified']
    fields = ('key', 'url', 'created', 'modified')
