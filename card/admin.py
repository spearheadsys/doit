from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from card.models import Card, Worklog, Priority, Column, Task, Columntype, Reminder
from django.contrib.auth.models import User
from contact.models import UserProfile


# class ProfileInline(admin.StackedInline):
# 	model = UserProfile
# 	can_delete = False
# 	verbose_name_plural = 'profile'


class CardAdmin(admin.ModelAdmin):
    model = Card
    list_display = ('title', 'board', 'owner')


class ColumnAdmin(admin.ModelAdmin):
    list_display = ('title', 'board', 'order', 'usage')


class ReminderAdmin(admin.ModelAdmin):
    list_display = ('reminder_time', 'card', 'owner')


# Define a new User admin
# class UserAdmin(admin.ModelAdmin):
# 	inlines = (ProfileInline, )

admin.site.register(Card, CardAdmin)
admin.site.register(Column, ColumnAdmin)
admin.site.register(Worklog)
admin.site.register(Priority)
admin.site.register(Task)
admin.site.register(Columntype)
admin.site.register(Reminder, ReminderAdmin)

# admin.site.unregister(User)
# admin.site.register(User)
# +, UserAdmin
