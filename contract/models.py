from django.db import models
from organization.models import Organization
from datetime import datetime
from django.contrib.auth.models import User

# Create your models here.
class Contract(models.Model):
    """ A commercial contract. """
    name = models.CharField(max_length=255, null=True, blank=True)
    company = models.ForeignKey(Organization, null=True, blank=True)
    # TODO: what things are required for a contract?
    # start date
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    created_by = models.ForeignKey(User, related_name="contract_created_by_user")
    owner = models.ForeignKey(User, null=True, blank=True)
    active = models.BooleanField()
    sla = models.ForeignKey("Sla", null=True, blank=True)

    def __unicode__(self):
        return self.name

class Sla(models.Model):
    """
    A single SLA entry.
    """
    name = models.CharField(max_length=255, null=True, blank=True)
    response_time = models.IntegerField()
    repair_time = models.IntegerField()
    # default = models.OneToOneField(Contract)

    def __unicode__(self):
        return self.name
