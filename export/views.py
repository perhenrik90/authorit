from django.shortcuts import render, redirect
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse
from django.template import RequestContext, loader, Template, Context
from django.http import HttpResponse

from authorit import settings
from cbuilder.models import Course, Slide

def preview(request):

    c = {}

    if 'pid' in request.GET:
        pid = request.GET['pid']
        course = Course.objects.get(id=pid)
        c["course"] = course
        c["slides"] = Slide.objects.filter(course=course).order_by("number")
        
    else:
        c["message"] = _("Course not found!")

    x = open(settings.MEDIA_ROOT+"file.xml","w")
    x.write("<html></html>")

    template = loader.get_template("slides.html")
    context = RequestContext(request, c)
    return HttpResponse(template.render(context))
