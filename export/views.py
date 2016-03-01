from django.shortcuts import render, redirect
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse
from django.template import RequestContext, loader, Template, Context
from django.http import HttpResponse
from django.utils.encoding import smart_str

from authorit import settings
from cbuilder.models import Course, Slide, Image
from export.models import Build

from export.scorm import SCORM

def preview(request):

    c = {}

    if 'pid' in request.GET:
        pid = request.GET['pid']
        course = Course.objects.get(id=pid)
        c["course"] = course
        c["slides"] = Slide.objects.filter(course=course).order_by("number")

        
    else:
        c["message"] = _("Course not found!")


    template = loader.get_template("slides.html")
    context = RequestContext(request, c)
    return HttpResponse(template.render(context))


#
# Do an SCORM export!
#
def export_scorm(request):
    c = {}
    
    if 'pid' in request.GET:
        pid = request.GET['pid']
        course = Course.objects.get(id=pid)
        c["course"] = course
        c["slides"] = Slide.objects.filter(course=course).order_by("number")
        c["images"] = Image.objects.filter(course=course)
        
        sco = SCORM(course, c["slides"], c["images"])
        path = sco.export_scorm()

        build = Build(course=course, build_path=path)
        build.save()
        
        response = HttpResponse(content_type='application/force-download')
        response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(course.code+'.zip')
	response.write(open(path,"rb").read())

        response['X-Sendfile'] = smart_str(path)

        return response
