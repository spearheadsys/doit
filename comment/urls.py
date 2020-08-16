from django.conf.urls import url
from comment.views import comment, add_comment, get_comment, \
	get_comment_count, delete_comment

# we are at /comments here
urlpatterns = [
	url(r'^$', comment, name='comment'),
	url(r'addcomment', add_comment, name='comment'),
	url(r'getcomments', get_comment, name='get comment'),
	url(r'getcommentcount', get_comment_count, name='get comment count'),
	url(r'delete/(?P<comment>\d+)', delete_comment, name='delete comment'),
]
