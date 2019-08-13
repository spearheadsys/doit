from django.db import models
from django.contrib.auth.models import User


class Organization(models.Model):
    """ An Organization. """
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
    owner = models.ForeignKey(User, related_name="organization_owner")
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
    boards = models.ManyToManyField(to='board.Board', related_name='organization_boards')
    # TODOD: when deleting/de-activating  a company we must manually remove associated domains or make them inactive!
    email_domains = models.ManyToManyField(to='EmailDomain', related_name='email_domain', blank=True)
    allow_external_contacts = models.BooleanField(default=False)
    allow_auto_contact_creation = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name


class EmailDomain(models.Model):
    domain = models.CharField(max_length=255, blank=True, null=True)

    def __unicode__(self):
        return self.domain
