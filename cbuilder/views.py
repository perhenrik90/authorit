from django.shortcuts import render
from django.shortcuts import render, redirect
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse
from django.template import RequestContext, loader, Template, Context
from django.http import HttpResponse, HttpResponseRedirect

from cbuilder.models import Course, Slide

#
# Describe a project
#
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



#
# View for editing slides
#
def edit_slide(request):

    c = {}

    if 'sid' in request.GET:
        sid = request.GET['sid']

        try:
            slide = Slide.objects.get(id=sid)
            c["slide"] = slide
        except Exception:
            c["message"] = _("Course with id %s not found!" % pid)

        # add next prev if it exsists!
        try:
            c["prev_slide"] = Slide.objects.get(number=slide.number-1, course=slide.course)
        except Exception:
            pass
            
        # add next slide if it exsists!
        try:
            c["next_slide"] = Slide.objects.get(number=slide.number+1, course=slide.course)
        except Exception:
            pass
            

    else:
        c["message"] = _("No slide id was given!")

    
    template = loader.get_template("edit_slide.html")
    context = RequestContext(request, c)
    return HttpResponse(template.render(context))	



def create_slide(request):

    c = {}

    if 'pid' in request.POST:
        try:
            pid = request.POST["pid"]
            course = Course.objects.get(id=pid)
            slide = Slide(title=request.POST["title"], course=course)

            # add a new slide number (at the end)
            slide.number = len(Slide.objects.filter(course=course))+1
            
            # add a default header
            slide.html = '<div class="row"><div id="wd1" class="col-sm-12"><h1>%s</h1></div></div>' % slide.title
            slide.save()

            # send the user to edit slide
            return HttpResponseRedirect(reverse('cbuilder.views.edit_slide')+"?sid=%s" % slide.id)            

        except Exception:
            c["message"] = _("Could not create a new slide to course %s" %course.title)
            
    # if no post are given
    if 'pid' in request.GET:
        try:
            pid = request.GET["pid"]
            c["course"] = Course.objects.get(id=pid)
        except Exception:
            c["message"] = _("Course with id %s not found!" % pid)

    else:
        c["message"] = _("No course id given. Can not create slide!")
    
    template = loader.get_template("create_slide.html")
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


##################
# Delete a slide
##################
def delete_slide(request):

    c = {}
    if 'sid' in request.POST:
        sid = request.POST["sid"]

        try:
            slide = Slide.objects.get(id=sid)
            slide.delete()
            return HttpResponseRedirect(reverse('cbuilder.views.project')+"?pid=%s" % slide.course.id)
        
        except Exception:
            c["message"] =  _("Could not find slide with id %s" % sid)
            
    return HttpResponseRedirect(reverse('default.views.dashboard'))
