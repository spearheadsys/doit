from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from card.models import Card, Worklog, Priority, Column, Columntype
from django.contrib.auth.models import User
from contact.models import UserProfile

class CardAdmin(admin.ModelAdmin):
    model = Card
    list_display = ('title', 'board', 'owner')


class ColumnAdmin(admin.ModelAdmin):
    list_display = ('title', 'board', 'order', 'usage')


class ReminderAdmin(admin.ModelAdmin):
    list_display = ('reminder_time', 'card', 'owner')

admin.site.register(Card, CardAdmin)
admin.site.register(Column, ColumnAdmin)
admin.site.register(Worklog)
admin.site.register(Priority)
admin.site.register(Columntype)
