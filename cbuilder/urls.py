from django.conf.urls import url

from . import views

subpath = "course/"


urlpatterns = [
    url(r'^project$', views.project, name='project'),
    url(r'^editslide$', views.edit_slide, name='edit slide'),
    url(r'^editslidetitle$', views.edit_slide_title, name='edit slide title'),
    url(r'^create_course$', views.create_course, name='create course'),
    url(r'^delete_course$', views.delete_course, name='delete course'),
    url(r'^createslide$', views.create_slide, name='create slide'),
    url(r'^saveslide$', views.save_slide, name='save slide'),
    url(r'^toglemenuslide$', views.toggle_menu_slide, name='togle menu slide'),
    url(r'^deleteslide$', views.delete_slide, name='delete slide'),
    url(r'^swapslide$', views.swap_slide, name='swap slide'),
    url(r'^upload_image$', views.upload_image, name='upload image'),
    url(r'^upload_video$', views.upload_video, name='upload video')
    
]
