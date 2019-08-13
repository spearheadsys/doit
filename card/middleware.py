import pytz
from contact.models import UserProfile
from django.contrib.auth.models import User

from django.utils import timezone
from django.utils.deprecation import MiddlewareMixin


class TimezoneMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_authenticated():
            u = User.objects.get(username=request.user)
            up = UserProfile.objects.get(user_id=u.id)
            tzname = up.timezone
            if tzname:
                timezone.activate(pytz.timezone(tzname))
            else:
                timezone.deactivate()
        else:
            timezone.deactivate()