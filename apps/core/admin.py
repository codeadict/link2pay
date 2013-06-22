# -*- coding: utf-8 -*-#
from django.contrib import admin
from core.models import UserProfile


class UserProfileAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_on'
    list_display = ('id', 'username', 'email', 'created_on')
    list_filter = list_display[3:]
    search_fields = list_display[:3]
    
admin.site.register(UserProfile, UserProfileAdmin)