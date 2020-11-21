from django import template
import hashlib
import urllib
from django import template
from django.utils.safestring import mark_safe

register = template.Library()


# return only the URL of the gravatar
# TEMPLATE USE:  {{ email|gravatar_url:150 }}
@register.filter
def gravatar_url(email, size=32):
    # todo: get default userprofile image
    # rememnber to alow selection: gravatar or custom image. or if custom image, do not use gravatar
    default = "https://example.com/static/images/defaultavatar.jpg"
    return "https://www.gravatar.com/avatar/%s?%s" % (hashlib.md5(email.lower().encode("utf-8")).hexdigest(), urllib.parse.urlencode({'d': default, 's': str(size)}))


# return an image tag with the gravatar
# TEMPLATE USE:  {{ email|gravatar:150 }}
@register.filter
def gravatar(email, size=32):
    url = gravatar_url(email, size)
    return mark_safe('<img src="%s" height="%d" width="%d">' % (url, size, size))
