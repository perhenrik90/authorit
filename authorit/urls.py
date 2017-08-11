from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls.static import  static

import default.views
import export.views

import settings

urlpatterns = [
    # Examples:
    # url(r'^$', 'authorit.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', default.views.login_view, name='login'),
    url(r'^dashboard$', default.views.dashboard, name='dashboard'),
    url(r'^search$', export.views.search_projects, name='search_projects'),

    url(r'^view/(?P<project>[\w-]+)/$', export.views.preview, name='preview'),
    url(r'^export_scorm$', export.views.export_scorm, name='export_scorm'),
    url(r'^import_scorm$', export.views.import_scorm, name='import_scorm'),

    url(r'^course/', include('cbuilder.urls')),

     url(r'^admin/', admin.site.urls),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
