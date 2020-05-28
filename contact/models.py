from django.db import models
from django.contrib.auth.models import User
from card.models import Organization
import os


def get_upload_path(instance, filename):
    print("PROFILE INSTANCE", instance)
    # path = 'uploads/{}/{}/{}'.format(related_card.board.id, related_card.id, uploaded_file)
    return os.path.join('customer_images', "%d" % instance.user.id, "%d", "%s" % filename)


# Create your models here.
class UserProfile(models.Model):
    """ Userprofile is a mapping to User. It adds a picture
    , relation to company, defines role (customer/admin)"""
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User, related_name='profile_user', on_delete=models.CASCADE)

    # TODO: every profile must have an image
    # get a default working
    # The additional attributes we wish to include.
    picture = models.ImageField(
        # change to profile
        upload_to='customer_images',
        blank=True,)

    import pytz
    TIMEZONES = tuple(zip(pytz.all_timezones, pytz.all_timezones))

    timezone = models.CharField(max_length=255, choices=TIMEZONES, default='Europe/Bucharest')

    # here we make the association with a company
    company = models.ForeignKey(
        Organization,
        null=True,
        blank=True,
        related_name='organization_related_name',
        on_delete=models.SET_NULL)

    # fav_boards = models.TextField()

    # NOTE TODO: is_superuser on UserProfile should be moved from user.is_superuser
    is_superuser = models.BooleanField(default=False)

    # is_operator defines this user as an agent/operator within doit
    # this allows user to "see" cards / boards assigned to him directly
    # or where he is a watcher
    is_operator = models.BooleanField(default=False)
 
    # define is this is a customer
    is_customer = models.BooleanField(default=False)

    # define if this is an org admin
    # user becomes administrator for organization
    is_org_admin = models.BooleanField(default=False)

    # is user on call?
    is_oncall = models.BooleanField(default=False)

    # is user on call?
    is_automation_user = models.BooleanField(default=False)

    # def get_open_cards(self):
    #     cards = Card.objects.all().filter(closed=False, owner=self.user).count()
    #     return cards

    # Override the __unicode__() method to return out something
    # meaningful!
    def __str__(self):
        return self.user.username
