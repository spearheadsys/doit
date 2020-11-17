from django import template
import hashlib
import urllib
from django import template
from django.utils.safestring import mark_safe
from django.contrib.staticfiles.finders import find as find_static_file
from django.conf import settings
from bs4 import BeautifulSoup
import ast

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


#Todo: work these out
# emails do not contain images although the URL\s are correct
# thought this was due to the remote rendering server not being signed in
# but local emails are also not rendered
# https://blog.khophi.co/datalize-your-images-in-django/ # <- could help
@register.filter
def find_all_images_in_template(template):
    bs = BeautifulSoup(template)
    soup = bs.find_all('figure')
    for figure in soup:
        if figure.img:
            figure.img.replace_with('<p style="text-decoration: underline">[ Attachment stripped. Login to DoIT to view. ]</p>')
        # else:
            # todo: do we need to do anything here?
            # attachment was not of type image
            # figure["data-trix-attachment"]
            # print(ast.literal_eval(figure.attrs["data-trix-attachment"])['url'])
    return soup


@register.simple_tag
def encode_static(path, encoding='base64', file_type='image'):
    """
    a template tag that returns a encoded string representation of a staticfile
    Usage::
        {% encode_static path [encoding] %}
    Examples::
        <img src="{% encode_static 'path/to/img.png' %}">
    """
    try:
        file_path = find_static_file(path)
        ext = file_path.split('.')[-1]
        file_str = get_file_data(file_path).encode(encoding)
        return u"data:{0}/{1};{2},{3}".format(file_type, ext, encoding, file_str)
    except IOError:
        return ''


@register.simple_tag
def raw_static(path):
    """
    a template tag that returns a raw staticfile
    Usage::
        {% raw_static path %}
    Examples::
        <style>{% raw_static path/to/style.css %}</style>
    """
    try:
        if path.startswith(settings.STATIC_URL):
            # remove static_url if its included in the path
            path = path.replace(settings.STATIC_URL, '')
        file_path = find_static_file(path)
        return get_file_data(file_path)
    except IOError:
        return ''


def get_file_data(file_path):
    with open(file_path, 'rb') as f:
        data = f.read()
        f.close()
        return data