# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse
from django.template import RequestContext, loader, Template, Context
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.encoding import smart_text

from default.views import login_view
from cbuilder.models import Course, Slide,Image

#
# View a project
#
def project(request):

    c = {}
    if not request.user.is_authenticated():
        c["message"] = _("You must be logged in to see this page")
        return redirect(login_view)
    
    if "pid" in request.GET:
        pid = request.GET["pid"]

        try:
            c["course"] = Course.objects.get(id=pid)
            c["slides"] = Slide.objects.filter(course=c["course"]).order_by('number')
            c["images"] = Image.objects.filter(course=c["course"])

            # Set up references to next and previous slides
            for i in range(len(c["slides"])):

                if i < len(c["slides"])-1:
                    c["slides"][i].nextSlide = c["slides"][i+1]
                if i > 1:
                    c["slides"][i].prevSlide = c["slides"][i-1]
                    
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
    if not request.user.is_authenticated():
        c["message"] = _("You must be logged in to see this page")
        return redirect(login_view)
    
    if 'sid' in request.GET:
        sid = request.GET['sid']

        try:
            slide = Slide.objects.get(id=sid)
            c["slide"] = slide
            c["images"] = Image.objects.filter(course=slide.course)

            
        except Exception:
            c["message"] = _("Course with id %s not found!" % sid)

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


def create_course(request):
    c = {}
    if not request.user.is_authenticated():
        c["message"] = _("You must be logged in to see this page")
        return redirect(login_view)


    if 'title' in request.POST:

        co = Course(title=request.POST["title"],
                   description=request.POST["description"],
                   code=request.POST["code"],
                   owner=request.user)

        try:
            co.save()
            return redirect(login_view)
        except Exception:
            c["message"] = _("Can not create the project. The course code is not unique!")
        
    
    template = loader.get_template("create_course.html")
    context = RequestContext(request, c)
    return HttpResponse(template.render(context))	
    



########################
# Creates a new slide
########################
def create_slide(request):
    if not request.user.is_authenticated():
        c["message"] = _("You must be logged in to see this page")
        return redirect(login_view)
    
    c = {}

    if 'pid' in request.POST:
        try:
            # try to get model from id
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

        html = smart_text(html)
        
        slide = Slide.objects.get(id=sid)
        slide.html = html
        slide.save()
        return HttpResponseRedirect(reverse('cbuilder.views.edit_slide')+"?sid=%s" % slide.id)


##################
# Delete a slide
##################
def delete_slide(request):
    c = {}
    if not request.user.is_authenticated():
        c["message"] = _("You must be logged in to see this page")
        return redirect(login_view)

    
    if 'sid' in request.POST:
        sid = request.POST["sid"]

        try:
            slide = Slide.objects.get(id=sid)
            slide.delete()
            return HttpResponseRedirect(reverse('cbuilder.views.project')+"?pid=%s" % slide.course.id)
        
        except Exception:
            c["message"] =  _("Could not find slide with id %s" % sid)
            
    return HttpResponseRedirect(reverse('default.views.dashboard'))


def swap_slide(request):

    c = {}
    if not request.user.is_authenticated():
        c["message"] = _("You must be logged in to see this page")
        return redirect(login_view)

    if 'sid1' in request.POST and 'sid2' in request.POST:
        sid1 = request.POST['sid1']
        sid2 = request.POST['sid2']

        slide1 = Slide.objects.get(id=sid1)
        slide2 = Slide.objects.get(id=sid2)

        # swap the slide numbers
        t1 = slide1.number
        t2 = slide2.number
        slide1.number = 10000000
        slide1.save()
        slide2.number = t1
        slide2.save()
        slide1.number = t2
        slide1.save()

        return HttpResponseRedirect(reverse('cbuilder.views.project')+"?pid=%s" % slide1.course.id)

    return HttpResponseRedirect(reverse('default.views.dashboard'))
