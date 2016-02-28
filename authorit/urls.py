from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'authorit.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^dashboard$', 'default.views.dashboard', name='dashboard'),
    url(r'^course/', include('cbuilder.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
