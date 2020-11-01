from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from doit.views import user_login, user_logout, profile
from contact.views import change_password
from django.conf.urls import include, url
from doit.views import home
from doit.views import getCardsCreatedToday, getWlogsCreatedToday, closed_cards_ajax, \
    overdue_cards_ajax, open_incidents_ajax, open_cards_dt, settings_view, my_vue_cards, \
    profile_change_picture, cards_without_owner, cards_without_company, my_incidents, all_my_open_cards, \
    my_overdue_cards_list, protected_serve
from django.contrib import admin
from .routers import router
admin.autodiscover()


urlpatterns = [
    url(r'^$', home, name='home'),
    # email viewer
    # url(r'emailviewer$', emailviewer, name='emailviewer'),

    # Todo: merge with cards (urls, etc)
    url(r'^closed_cards_ajax', closed_cards_ajax, name='closed_cards_ajax'),
    url(r'^overdue_cards_ajax', overdue_cards_ajax, name='overdue_cards_ajax'),
    url(r'^open_incidents_ajax', open_incidents_ajax, name='open_incidents_ajax'),
    url(r'^open_cards_dt', open_cards_dt, name='open_cards_dt'),
    url(r'^cards/all_my_open_cards', all_my_open_cards, name='all_my_open_cards'),
    url(r'^my_vue_cards', my_vue_cards, name='my_vue_cards'),
    # url(r'^my_vue_overdue', my_vue_overdue, name='my_vue_overdue'),
    url(r'^cards/my_overdue_cards_list', my_overdue_cards_list, name='my_overdue_cards_list'),
    url(r'^cards/cards_without_owner', cards_without_owner, name='cards_without_owner'),
    url(r'^cards/cards_without_company', cards_without_company, name='cards_without_company'),
    url(r'^cards/my_incidents', my_incidents, name='my_incidents'),

    url(r'^settings', settings_view, name='settings_view'),

    url(r'^%s(?P<path>.*)$' % settings.MEDIA_URL[1:], protected_serve, {'document_root': settings.MEDIA_ROOT}),

    # TODO: move these to 'global' api project?
    # url(r'^api/get_todays_cards/',
    #     getCardsCreatedToday,
    #     name='getCardsCreatedToday'),
    # url(r'^api/get_todays_wlogs/', getWlogsCreatedToday, name='getWlogsCreatedToday'),
    # url(r'^api/get_todays_tasks/', getTodaysTasks, name='getTodaysTasks'),

    # login / logout
    url(r'^login/$', user_login, name='login'),
    url(r'^logout/$', user_logout, name='logout'),

    # profile
    url(r'^profile/$', profile, name='profile'),
    url(r'^profile/password/$', change_password, name='change_password'),
    url(r'^profile/picture/$', profile_change_picture, name='profile_change_picture'),

    # admindocs
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # admin page
    url(r'^admin/', admin.site.urls),
    # include contacts
    url(r'^contacts/', include('contact.urls')),
    # organizations
    url(r'^organizations/', include('organization.urls')),
    # cases
    url(r'^cards/', include('card.urls')),
    # boards / projects
    url(r'^boards/', include('board.urls')),
    # include analytics
    url(r'^analytics/', include('analytics.urls')),
    # attachments
    url(r'^attachments/', include('attachment.urls')),
    # comments or notes
    url(r'^comments/', include('comment.urls')),

    #
    # test rest,vue
    #
    url(r'^api2/', include(router.urls)),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# if settings.DEBUG:
#     import debug_toolbar
#     urlpatterns += [
#         url(r'^__debug__/', include(debug_toolbar.urls)),
#     ]

urlpatterns += staticfiles_urlpatterns()
