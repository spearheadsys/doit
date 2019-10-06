from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from doit.views import user_login, user_logout, profile
from contact.views import change_password
from django.conf.urls import include, url
from doit.views import home
from doit.views import getCardsCreatedToday, getWlogsCreatedToday, getTodaysTasks, emailviewer, closed_cards_ajax, \
    overdue_cards_ajax, open_incidents_ajax, open_cards_ajax, settings_view, my_vue_cards, my_vue_overdue
from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    url(r'^$', home, name='home'),
    # email viewer
    url(r'emailviewer$', emailviewer, name='emailviewer'),

    url(r'^summernote/', include('django_summernote.urls')),

    url(r'^closed_cards_ajax', closed_cards_ajax, name='closed_cards_ajax'),
    url(r'^overdue_cards_ajax', overdue_cards_ajax, name='overdue_cards_ajax'),
    url(r'^open_incidents_ajax', open_incidents_ajax, name='open_incidents_ajax'),
    url(r'^open_cards_ajax', open_cards_ajax, name='open_cards_ajax'),
    url(r'^my_vue_cards', my_vue_cards, name='my_vue_cards'),
    url(r'^my_vue_overdue', my_vue_overdue, name='my_vue_overdue'),

    url(r'^settings', settings_view, name='settings_view'),

    # TODO: move these to 'global' api project?
    url(r'^api/get_todays_cards/', 
        getCardsCreatedToday, 
        name='getCardsCreatedToday'),
    url(r'^api/get_todays_wlogs/', getWlogsCreatedToday, name='getWlogsCreatedToday'),
    url(r'^api/get_todays_tasks/', getTodaysTasks, name='getTodaysTasks'),

    # login / logout
    url(r'^login/$', user_login, name='login'),
    url(r'^logout/$', user_logout, name='logout'),
    # profile
    url(r'^profile/$', profile, name='profile'),
    url(r'^profile/password/$', change_password, name='change_password'),
    # admindocs
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # admin page
    url(r'^admin/', include(admin.site.urls)),
    # include contacts
    url(r'^contacts/', include('contact.urls')),
    # organizations
    url(r'^organizations/', include('organization.urls')),
    # cases
    url(r'^cards/', include('card.urls')),
    # boards / projects
    url(r'^boards/', include('board.urls')),
    # include reports
    url(r'^reports/', include('report.urls')),
    # TODO: disable / replace omcpletely inplace editing
    # url(r'^inplaceeditform/', include('inplaceeditform.urls')),
    # attachments
    url(r'^attachments/', include('attachment.urls')),
    # comments or notes
    url(r'^comments/', include('comment.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# if settings.DEBUG:
#     import debug_toolbar
#     urlpatterns += [
#         url(r'^__debug__/', include(debug_toolbar.urls)),
#     ]

urlpatterns += staticfiles_urlpatterns()
