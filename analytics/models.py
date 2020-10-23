from django.db import models
from django.contrib.auth.models import User
from board.models import Board
from organization.models import Organization


# cards
class Reports(models.Model):
    """
    Stores a single analytics entry.
    """
    title = models.CharField(max_length=255)
    description = models.TextField()
    company = models.ForeignKey(Organization, models.CASCADE)
    # we should get this automatically form assigned in user
    #  and allow only admins to view reports
    owner = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    # we only save the period and board form which to
    # generate the analytics
    period_from = models.DateTimeField()
    period_to = models.DateTimeField(null=True, blank=True)
    board = models.ForeignKey(Board, models.CASCADE)

    def __unicode__(self):
        return self.title

