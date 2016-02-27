from django.conf.urls import url

from . import views

subpath = "course/"


urlpatterns = [
    url(r'^project$', views.project, name='project'),
    url(r'^editslide$', views.edit_slide, name='edit slide'),
    url(r'^saveslide$', views.save_slide, name='save slide')
]
