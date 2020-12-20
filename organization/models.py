from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from taggit.managers import TaggableManager


class Organization(models.Model):
    """ An Organization. """

    class Meta:
        ordering = ['name']

    name = models.CharField(max_length=255)
    billing_address = models.CharField(max_length=255, blank=True, null=True)
    billing_zip_code = models.CharField(max_length=24, blank=True, null=True)
    billing_city = models.CharField(max_length=255, blank=True, null=True)
    billing_country = models.CharField(max_length=255, blank=True, null=True)
    # when necessary
    # shipping_address =  models.CharField(max_length=255)
    bank = models.CharField(max_length=255, blank=True, null=True)
    iban = models.CharField(max_length=64, blank=True, null=True)
    registration_code = models.CharField(max_length=128, blank=True, null=True)
    vat_number = models.CharField(max_length=128, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    active = models.BooleanField(default=True)
    contacts = models.ManyToManyField(to=User, related_name='organization_contacts', blank=True)
    owner = models.ForeignKey(User, related_name="organization_owner", null=True, on_delete=models.SET_NULL)
    created_time = models.DateField(auto_now=True)
    modified_time = models.DateField(auto_now_add=True)
    priority = models.IntegerField(blank=True, null=True)
    logo = models.ImageField(
        upload_to='logos',
        blank=True,)
    default_board = models.ForeignKey(
        'board.Board',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    csat_exclude = models.BooleanField(blank=False,null=False,default=False)
    included_hours = models.IntegerField(blank=True, null=True)
    # used hours is in-app calculation
    sla_name = models.CharField(max_length=255, blank=True, null=True)
    sla_response_time = models.IntegerField(blank=True, null=True)
    # TODO: add # sla_resolution_time = models.IntegerField(blank=True, null=True)
    boards = models.ManyToManyField(to='board.Board', related_name='organization_boards')
    # TODOD: when deleting/de-activating  a company we must manually remove associated domains or make them inactive!
    email_domains = models.ManyToManyField(to='EmailDomain', related_name='email_domain', blank=True)
    allow_external_contacts = models.BooleanField(default=False)
    allow_auto_contact_creation = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class KnowledgeBase(models.Model):
    name = models.CharField(max_length=255)
    public = models.BooleanField(blank=False, null=False, default=False)
    company = models.ForeignKey(Organization, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name


class KnowledgeBaseCategory(models.Model):
    name = models.CharField(max_length=255)
    company = models.ForeignKey(Organization, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name


class KnowledgeBaseArticle(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(KnowledgeBaseCategory, null=False, blank=False, on_delete=models.CASCADE)
    knowledgebase = models.ForeignKey(KnowledgeBase, null=True, blank=False, on_delete=models.SET_NULL)
    related_cards = models.ManyToManyField(to='card.Card', related_name='kb_article', blank=True)
    likes = models.IntegerField(default=0)
    favorite = models.BooleanField(blank=True, null=True, default=False)
    showcase = models.BooleanField(blank=True, null=True, default=False)
    published_date = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    last_update_date = models.DateTimeField(blank=True, null=True, auto_now=True)
    content = models.TextField(null=True, blank=True)
    tags = TaggableManager(blank=True)

    class KBArticleState(models.TextChoices):
        DRAFT = 'DR', _('Draft')
        PUBLISHED = 'PB', _('Published')
        PRIVATE = 'PR', _('Private')
        ARCHIVED = 'AR', _('Archived')

    state = models.CharField(max_length=2, choices=KBArticleState.choices, default=KBArticleState.DRAFT)

    def __str__(self):
        return self.name


class EmailDomain(models.Model):
    domain = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.domain
