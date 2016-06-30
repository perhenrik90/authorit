from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf.urls.static import  static

import settings

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'authorit.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', 'default.views.login_view', name='login'),
    url(r'^dashboard$', 'default.views.dashboard', name='dashboard'),

    url(r'^view/(?P<project>[\w-]+)/$', 'export.views.preview', name='preview'),
    url(r'^export_scorm$', 'export.views.export_scorm', name='export_scorm'),


    url(r'^course/', include('cbuilder.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
