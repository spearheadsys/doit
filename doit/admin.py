from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from doit.models import Tracker
from django.contrib.auth.models import User
from contact.models import UserProfile


# class ProfileInline(admin.StackedInline):
# 	model = UserProfile
# 	can_delete = False
# 	verbose_name_plural = 'profile'


class TrackerAdmin(admin.ModelAdmin):
    model = Tracker
    list_display = (
        'object_id',
        'action',
        'updated_fields',
        # 'ordering'
    )


# owner = models.ForeignKey(User, null=False, blank=False)
#     content_type = models.ForeignKey(ContentType)
#     object_id = models.PositiveIntegerField()
#     content_object = GenericForeignKey('content_type', 'object_id')
#     created_time = models.DateTimeField(auto_now_add=True, null=True)
#     # actions are usually the view name...
#     # look for # TRACKER start/end comments
#     action = models.CharField(max_length=150, blank=True, null=True)
#     updated_fields = models.TextField()
# ordering =  ordering = ['-created_time']

admin.site.register(Tracker, TrackerAdmin)

# admin.site.unregister(User)
# admin.site.register(User)
# +, UserAdmin
