from django.contrib import admin
from contact.models import UserProfile


class UserProfileAdmin(admin.ModelAdmin):
    search_fields = ['user__email', 'user__first_name', 'user__last_name']


# Register your models here.
admin.site.register(UserProfile, UserProfileAdmin)
