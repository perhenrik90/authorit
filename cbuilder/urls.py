from django.conf.urls import url

from . import views

subpath = "course/"


urlpatterns = [
    url(r'^project$', views.project, name='project'),
    url(r'^editslide$', views.edit_slide, name='edit slide'),
    url(r'^createslide$', views.create_slide, name='create slide'),
    url(r'^saveslide$', views.save_slide, name='save slide'),
    url(r'^deleteslide$', views.delete_slide, name='delete slide'),
    url(r'^swapslide$', views.swap_slide, name='swap slide')
]
