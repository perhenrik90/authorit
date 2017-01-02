# -*- coding: utf-8 -*-
from io import StringIO

from django.shortcuts import render, redirect
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse
from django.template import RequestContext, loader, Template, Context
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.encoding import smart_str

from authorit import settings
from cbuilder.models import Course, Slide, Image, Video
from export.models import Build

import cbuilder.views
from export.scorm import SCORM_Export, SCORM_Import

#
# Preview a project
#
def preview(request, project):

    c = {}

    if(project == ""):
        c["message"] = _("Course not found!")


    else:

        course = Course.objects.get(code=project)

        c["course"] = course
        c["slides"] = Slide.objects.filter(course=course).order_by("number")


    template = loader.get_template("slides.html")
    context = RequestContext(request, c)
    return HttpResponse(template.render(context))



#
# Search in projects (as staff)
#
def search_projects(request):
    c = {}

    template = loader.get_template("search_project.html")
    context = RequestContext(request, c)

    if('q' in request.GET):
        query = request.GET["q"]
        c["courses"] = Course.objects.filter(title__icontains=query)

    
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
        c["videos"] = Video.objects.filter(course=course)
        
        sco = SCORM_Export(course, c["slides"], c["images"], c["videos"])
        path = sco.export_scorm()

        build = Build(course=course, build_path=path)
        build.save()
        
        response = HttpResponse(content_type='application/force-download')
        response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(course.code+'.zip')
	response.write(open(path,"rb").read())

        response['X-Sendfile'] = smart_str(path)
        return response


# import an SCORM zipfile and create a new course
def import_scorm(request):

    c = {}

    if 'code' in request.POST:
        ffile = request.FILES["zip"]
        code = request.POST["code"]
        
        new_course = SCORM_Import(request.user, code,ffile)
        return HttpResponseRedirect(reverse(cbuilder.views.project)+"?pid="+str(new_course.id))
    
    template = loader.get_template("upload_scorm.html")
    context = RequestContext(request, c)
    return HttpResponse(template.render(context))
