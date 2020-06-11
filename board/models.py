from django.db import models
from django.contrib.auth.models import User
from organization.models import Organization
from django.utils import timezone
#from django_mailbox.models import Mailbox


# Create your models here.
class Board(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    created_time = models.DateField(auto_now=True)
    modified_time = models.DateTimeField(auto_now_add=True)
    company = models.ForeignKey(Organization,
                                related_name='board_organization',
                                null=True,
                                blank=True,
                                on_delete=models.SET_NULL)
    # TODO: change this to User! currently we require two dal automcomplete to 
    # handle this specific relationship
    # contacts = models.ManyToManyField(User, null=True, blank=True, related_name="contact")
    archived = models.BooleanField(default=False)
    due_date = models.DateTimeField(null=True, blank=True)
    owner = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    order = models.IntegerField(null=True, blank=True)
    #mailbox = models.ForeignKey(Mailbox, related_name="Mailbox", null=True, blank=True, on_delete=models.SET_NULL)
    BOARD_CHOICES = (
        ('project_board', 'Project Board'),
        ('ongoing_board', 'Ongoing Board'),
        ('sales_board', 'Sales Board'),
    )
    type = models.CharField(max_length=128, choices=BOARD_CHOICES, default='ongoing_board', blank=False)

    # TODO: in html widgets we show the value not the name.
    # either of which are quite useless unless you know hex colors in your head.
    # we need to show the color when selecting (html select->option)
    COLOR_CHOICES = (
        ('0', 'Choose a color for this Board'),
        ('CORNSILK', '#fff8dc'),
        ('HONEYDUE', '#f0fff0'),
        ('MINTCREAM', '#f5fffa'),
        ('LAVENDER', '#e6e6fa'),
        ('LIGHTSTEEL', '#b0c4de'),
        ('DARNERTAIL', '#74b9ff'),
        ('CHIGONG', '#d63031'),
        ('SOOTHING', '#b2bec3'),
        ('SHY', '#a29bfe'),
    )
    color = models.CharField(max_length=12, choices=COLOR_CHOICES, default='CORNSILK', blank=True)

    def __str__(self):
        return self.name

    def get_archived(self):
        if self.archived is None:
            return None
        return bool(self.result)

    # TODO: this may miss out on certain boards overdue at 00:00:00 on same day, same with cards
    @property
    def is_overdue(self):
        today_date = timezone.now()
        if self.due_date and self.due_date < today_date:
            return True
        return False


class Meta:
    app_label = "board"
