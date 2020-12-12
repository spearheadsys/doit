from django.conf.urls import url
from attachment.views import attachments, addattachments, get_attachments, addkbattachments

urlpatterns = [
	url(r'^$', attachments, name='attachments'),
	url(r'addattachments/', addattachments, name='addattachments'),
	url(r'addkbattachments/', addkbattachments, name='addkbattachments'),
	url(r'getattachments', get_attachments, name='get attachments'),
]
