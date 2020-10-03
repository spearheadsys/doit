from django.db import models
from organization.models import Organization
from django.contrib.auth.models import User
from board.models import Board
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.db.models import Max, Sum
from comment.models import Comment
from taggit.managers import TaggableManager
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from attachment.models import Attachment
import os
from django.conf import settings
from shutil import rmtree


# cards
class Card(models.Model):
    """
    Stores single card entry. A card is analogous to a ticket/incident.
    """
    title = models.CharField(max_length=255)
    description = models.TextField()
    company = models.ForeignKey(Organization, null=True, blank=True, on_delete=models.SET_NULL)
    # incident, service request
    SERVICE_REQUEST = 'SR'
    INCIDENT = 'IN'

    TYPE_CHOICES = (
        (SERVICE_REQUEST, 'Service Request'),
        (INCIDENT, 'Incident'),
    )
    type = models.CharField(
        max_length=2,
        choices=TYPE_CHOICES,
        default=SERVICE_REQUEST,
        blank=True)

    watchers = models.ManyToManyField(
        User,
        blank=True,
        related_name="Watchers"
    )

    # todo: remove this when appropriate -use watchers instead
    owner = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    created_by = models.ForeignKey(User, related_name="created_by_user", null=True, on_delete=models.SET_NULL)
    start_time = models.DateTimeField(null=True, blank=True)
    due_date = models.DateTimeField(null=True, blank=True)
    priority = models.ForeignKey("Priority", blank=True, null=True, on_delete=models.SET_NULL)
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)
    board = models.ForeignKey(Board, related_name="card_board", on_delete=models.CASCADE)
    column = models.ForeignKey("Column", related_name="card_column", on_delete=models.PROTECT)
    closed = models.BooleanField(default=False)
    estimate = models.IntegerField(null=True, blank=True)
    order = models.IntegerField(null=True, blank=True)
    tags = TaggableManager(blank=True)
    csat = models.BooleanField()

    def __str__(self):
        return self.title

    # get worked minutes total
    def total_minutes(self):
        ctype = ContentType.objects.get_for_model(self)
        comments = Comment.objects.filter(
            content_type__pk=ctype.id,
            object_id=self.id)
        total_minutes_worked = comments.filter(billable=True).aggregate(Sum('minutes'))
        return total_minutes_worked['minutes__sum']

    def percent_of_estimate(self):
        if not self.total_minutes():
            return None
        try:
            perc = (self.total_minutes() / float("%0.2f" % self.estimate)) * 100
            return float("%0.2f" % perc)
        except TypeError:
            return None

    def sla_response_time(self):
        # TODO: how/where do I get time(period) when card was in column that should not add time? (such as waiting)
        # 1. get organization SLA
        # 2. calculate time card has been in backlog, queue, documentation
        # 3. diff 2 -1 and calculate whether we are ok or not
        if self.company.sla_response_time:
            return self.company.sla_response_time

    # def sla_percent(self):
    #     # idthratio card.age card.sla_response_time 100
    #     if not self.sla_response_time():
    #         return None
    #     perc = (float(self.age()) / float(self.sla_response_time())) * 100
    #     return float("%0.2f" % perc)

    def has_open_tasks(self):
        card = self
        ctype = ContentType.objects.get_for_model(Card)
        tasks = Task.objects.filter(
            content_type__pk=ctype.id,
            object_id=card.id,
            done=False)
        return tasks.count()

    def has_open_reminders(self):
        card = self
        reminders = Reminder.objects.filter(
            card=card.id,
            notified=False)
        return reminders.count()

    def age(self):
        from datetime import timedelta
        today = timezone.now()
        age = today - self.created_time
        # TODO: how/where do I get time(period) when card was in column that should not add time? (such as waiting)
        return int(age.total_seconds() / 60)

    def time_worked(self):
        ctype = ContentType.objects.get_for_model(Card)
        comments = Comment.objects.filter(
            content_type__pk=ctype.id,
            object_id=self.id
        )
        return comments.aggregate(Sum('minutes'))

    # used in templates to test if card.is_overdue in which case
    # we display a little red triangle
    # todo this comparison needs to be fined tuned (I htink we miss out certain cards 00:000:00 for ex)
    @property
    def is_overdue(self):
        today_date = timezone.now()
        if self.due_date and self.due_date < today_date:
            return True
        return False

    @property
    def is_done(self):
        # get the column order and identify done column
        # we assume this to be the right most column...
        board_done_order = Column.objects.filter(
            board=self.board).aggregate(Max('order'))['order__max']
        board_done_column = Column.objects.get(
            board=self.board,
            order=board_done_order)
        if self.column_id == board_done_column.id:
            return True
        return False

    # def delete(self, *args, **kwargs):
    #     self.card.delete()
    #     super(Attachment, self).delete(*args, **kwargs)

    class Meta:
        ordering = ['created_time']


def _delete_file(path):
   """ Deletes file from filesystem. """
   if os.path.isfile(path):
       os.remove(path)

@receiver(pre_delete, sender=Card)
def submission_delete(sender, instance, **kwargs):
    for a in Attachment.objects.filter(card=instance.id):
        a.content.delete(save=False)
        a.delete()
    cardpath = 'uploads/{}/{}'.format(instance.board.id, instance.id)
    if os.path.exists(os.path.join(settings.MEDIA_ROOT, cardpath)):
        rmtree(os.path.join(settings.MEDIA_ROOT, cardpath))
    

class Reminder(models.Model):
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    reminder_time = models.DateTimeField()
    card = models.ForeignKey(Card, related_name="card_reminder", on_delete=models.CASCADE)
    notified = models.BooleanField(default=False)

    def __str__(self):
        return str(self.created_time)


class Columntype(models.Model):
    name = models.CharField(max_length=255)
    created_time = models.DateField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Column(models.Model):
    """
    Stores a single column entry. A column is analogous to a project
    phase / ticket status.
    """

    title = models.CharField(max_length=50, blank=False, null=False)
    board = models.ForeignKey(Board, related_name="board_column", on_delete=models.CASCADE)
    wip = models.IntegerField(null=True, blank=True)
    order = models.IntegerField()
    # type (usage) of the column determines the workflows that are possible
    # a done column for example wold trigger notifications that a card
    # is closed
    # what if we get rid of type/usage alltogether and use workflows
    # that can be applied to any column? leave it up to the user?
    # Backlog/Queue (this is where they are queued)
    # Waiting (ticket is not being worked on pending some external event)
    # Done (ticket is closed)

    # TODO:
    # SPH (propunere de dezbatut) - tickeitng; un tichet mai vechi de 3 zile
    # treuie sa declanseze un eveniment: alerta / notificare;
    # un tichet in waiting/done trebuie sa anunte clientul ca NOI consideram
    # situatia fiind remediata/in asteptare si daca el mai asteapta ceva de la
    # noi (care este perspectiva clientului) sa ne anunte dand reply la tichet
    # sau sa dechida unul nou
    # usage = models.CharField(max_length=120, blank=True)
    usage = models.ForeignKey(Columntype, blank=True, null=True, related_name="column_usage", on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Priority(models.Model):
    """
    Stores a single priority entry. Analogous to ticket priority.
    """
    title = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.title


class Worklog(models.Model):
    """
    Stores a single worklog entry. A worklog is a unit of work.
    """
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    minutes = models.IntegerField(blank=True, null=True)
    overtime = models.BooleanField(default=False)
    billable = models.BooleanField()
    owner = models.ForeignKey(User, models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True, null=True)
    modified_time = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.description or u''


# todo: most likely will not use this to track
class CardTracker(models.Model):
    # TODO: when a card is deleted all of its history will also be deleted
    card = models.ForeignKey(Card, on_delete=models.CASCADE)

    # actions can be
    # create, delete, update
    # update includes
    # action = models.CharField(max_length=255)
    # owner = models.ForeignKey(User)
    # genericforeignkey kungfu
    # created_time = models.DateTimeField(auto_now_add=True, null=True)
    # updated_fields = models.TextField()

    def __str__(self):
        return self.card


class Task(models.Model):
    """
    Stores a simple task entry. It can be attached to any other object.
    """
    task = models.TextField()
    created_time = models.DateField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)
    done = models.BooleanField(default=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    # genericforeignkey kungfu
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return self.task
