from django.contrib import admin
from contact.models import UserProfile
from organization.models import Organization, KnowledgeBase, \
    KnowledgeBaseArticle, KnowledgeBaseCategory


class KBInline(admin.TabularInline):
    model = KnowledgeBase
    extra = 1


class ContactInline(admin.TabularInline):
    model = UserProfile
    extra = 1


class OrganizationAdmin(admin.ModelAdmin):
    model = Organization
    list_display = ('name', 'active', 'created_time')
    search_fields = ['name']
    inlines = [
        KBInline,
        ContactInline
    ]

    class Meta:
        ordering = ['created_time']


admin.site.register(Organization, OrganizationAdmin)
admin.site.register(KnowledgeBase)
admin.site.register(KnowledgeBaseCategory)
admin.site.register(KnowledgeBaseArticle)

