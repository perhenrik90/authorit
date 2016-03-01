from django.shortcuts import render, redirect
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse
from django.template import RequestContext, loader, Template, Context
from django.http import HttpResponse

from authorit import settings
from cbuilder.models import Course, Slide

from export.scorm import SCORM

def preview(request):

    c = {}

    if 'pid' in request.GET:
        pid = request.GET['pid']
        course = Course.objects.get(id=pid)
        c["course"] = course
        c["slides"] = Slide.objects.filter(course=course).order_by("number")
        sco = SCORM(course, c["slides"])
        sco.export_sco()
        
    else:
        c["message"] = _("Course not found!")




    template = loader.get_template("slides.html")
    context = RequestContext(request, c)
    return HttpResponse(template.render(context))


def export_scorm(request):

    if 'pid' in request.GET:
        pid = request.GET['pid']
        course = Course.objects.get(id=pid)
        c["course"] = course
        c["slides"] = Slide.objects.filter(course=course).order_by("number")
        sco = SCORM(course, c["slides"])
        sco.export_sco()

    response = HttpResponse(content_type='zip')
    response['Content-Disposition'] = 'attachment; filename="scorm.zip"'
