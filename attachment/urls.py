from django.conf.urls import url
from attachment.views import attachments, addattachments, get_attachments

urlpatterns = [
	url(r'^$', attachments, name='attachments'),
	url(r'addattachments/', addattachments, name='addattachments'),
	url(r'getattachments', get_attachments, name='get attachments'),
]
