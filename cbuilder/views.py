from django.shortcuts import render
from django.shortcuts import render, redirect
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse
from django.template import RequestContext, loader, Template, Context
from django.http import HttpResponse, HttpResponseRedirect

from cbuilder.models import Course, Slide

def project(request):

    c = {}

    if "pid" in request.GET:
        pid = request.GET["pid"]

        try:
            c["course"] = Course.objects.get(id=pid)
            c["slides"] = Slide.objects.filter(course=c["course"])
        except Exception:
            c["message"] = _("Course with id %s not found" % pid)
            
    else:
        c["message"] = _("Project id not given!")
        
    template = loader.get_template("project.html")
    context = RequestContext(request, c)
    return HttpResponse(template.render(context))	



def edit_slide(request):

    c = {}

    if 'sid' in request.GET:
        sid = request.GET['sid']
        slide = Slide.objects.get(id=sid)
        c["slide"] = slide
        

    else:
        c["message"] = _("No slide id was given!")

    
    template = loader.get_template("edit_slide.html")
    context = RequestContext(request, c)
    return HttpResponse(template.render(context))	



def save_slide(request):

    if 'html' in request.POST:
        html = request.POST["html"]
        sid = request.POST["sid"]

        slide = Slide.objects.get(id=sid)
        slide.html = html
        slide.save()
        return HttpResponseRedirect(reverse('cbuilder.views.edit_slide')+"?sid=%s" % slide.id)



        
