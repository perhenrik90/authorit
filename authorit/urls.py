from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'authorit.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^overview$', 'default.views.overview', name='overview'),
    
    url(r'^editslide$', 'cbuilder.views.edit_slide', name='edit slide'),
        
    url(r'^admin/', include(admin.site.urls)),
)
