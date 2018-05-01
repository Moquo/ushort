from django.contrib import admin
from .models import Url

class UrlAdmin(admin.ModelAdmin):
    list_display = ("url_id", "orig_url", "created_at", "clicks")

admin.site.register(Url, UrlAdmin)