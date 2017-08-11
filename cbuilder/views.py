# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse
from django.template import RequestContext, loader, Template, Context
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.encoding import smart_text
from django.contrib.auth.models import User

from default.views import login_view
from cbuilder.models import Course, Slide,Image, Video, CustomTheme

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
            c["videos"] = Video.objects.filter(course=c["course"])

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
    return HttpResponse(template.render(c,request))	


#
# View for edit project details
#
def edit_project(request):
    c = {}
    if not request.user.is_authenticated():
        c["message"] = _("You must be logged in to see this page")
        return redirect(login_view)

    if request.method == "POST":
        pid = request.POST["pid"]
        title = request.POST["title"]
        code = request.POST["code"]
        owner = request.POST["owner"]
        desc = request.POST["desc"]

        
        course = Course.objects.get(id=pid)
        course.title = title
        course.code = code
        course.owner = User.objects.get(username=owner)
        course.description = desc
        course.theme = None
        
        if request.POST["theme"] != 'none':
            theme = CustomTheme.objects.get(id=request.POST["theme"])
            course.theme = theme
            
        course.save()
        return HttpResponseRedirect(reverse('project')+"?pid="+str(course.id))
        
        
    if 'pid' in request.GET:
        c["course"] = Course.objects.get(id=request.GET["pid"])

    c["themes"] = CustomTheme.objects.all()
    
    template = loader.get_template("edit_project.html")
    return HttpResponse(template.render(c,request))	


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
            c["videos"] = Video.objects.filter(course=slide.course)
            
    
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
    return HttpResponse(template.render(c, request))	


def edit_slide_title(request):
    c = {}


    if 'title' in request.POST:
        sid = request.POST["sid"]
        title = request.POST["title"]

        slide = Slide.objects.get(id=sid)
        slide.title = title
        slide.save()

        return HttpResponseRedirect(reverse('project')+"?pid="+str(slide.course.id))
    
    if 'sid' not in request.GET:
        c["message"] = _("Slide id is not given!")
        template = loader.get_template("edit_slide_title.html")
        context = RequestContext(request, c)
        return HttpResponse(template.render(context))	

    sid = request.GET["sid"]
    c["slide"] = Slide.objects.get(id=sid)
          
    template = loader.get_template("edit_slide_title.html")
    return HttpResponse(template.render(c,request))	

#
# Toggle title on / of in menu
#
def toggle_menu_slide(request):

    if 'sid' in request.POST:
        sid = request.POST["sid"]
        slide = Slide.objects.get(id=sid)

        if slide.inMenu == True: slide.inMenu = False
        elif slide.inMenu == False: slide.inMenu = True

        slide.save()

    return HttpResponseRedirect(reverse('project')+"?pid="+str(slide.course.id))

#
# Create a new course
#
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
    return HttpResponse(template.render(c,request))	 

#
# Delete a course
#
def delete_course(request):
    c = {}
    
    if not request.user.is_authenticated():
        c["message"] = _("You must be logged in to see this page")
        return redirect(login_view)

    if 'cid' not in request.POST:
        c["message"] = _("Can not delete this course. Course not found!")

    if 'cid' in request.POST and 'confirm' in request.POST:
        course = Course.objects.get(id=request.POST['cid'])
        course.delete()
        return HttpResponseRedirect(reverse('dashboard'))
        
        
    if 'cid' in request.POST:
        c["course"] = Course.objects.get(id=request.POST['cid'])
        c["slides"] = Slide.objects.filter(course=c["course"])
    
    template = loader.get_template("delete_course.html")
    return HttpResponse(template.render(c,request))	 
    



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
            return HttpResponseRedirect(reverse('edit_slide')+"?sid=%s" % slide.id)            

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
    return HttpResponse(template.render(c,request))	



def save_slide(request):

    if 'html' in request.POST:
        html = request.POST["html"]
        sid = request.POST["sid"]

        html = smart_text(html)
        print(html)
        
        slide = Slide.objects.get(id=sid)
        slide.html = html
        slide.save()
        return HttpResponseRedirect(reverse('edit slide')+"?sid=%s" % slide.id)


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
            return HttpResponseRedirect(reverse('project')+"?pid=%s" % slide.course.id)
        
        except Exception:
            c["message"] =  _("Could not find slide with id %s" % sid)
            
    return HttpResponseRedirect(reverse('dashboard'))

#
# Swap two slides in order
#
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

        return HttpResponseRedirect(reverse('project')+"?pid=%s" % slide1.course.id)

    return HttpResponseRedirect(reverse('dashboard'))


#
# Image views
#
def upload_image(request):
    c = {}
    if not request.user.is_authenticated():
        c["message"] = _("You must be logged in to see this page")
        return redirect(login_view)


    if 'pid' in request.POST:

        try:

            pid = request.POST["pid"]
            course = Course.objects.get(id=pid)
            imgfile = request.FILES["img"]
            description = request.POST["description"]
        
            img = Image(course=course, img=imgfile, description=description)
            img.save()
            return HttpResponseRedirect(reverse('project')+"?pid=%s" % course.id)
        except Exception:
            c["message"] = _("Upload failed!")


    if 'pid' in request.GET:
        course = Course.objects.get(id=request.GET["pid"])
        c["course"] = course

    else:
        c["message"] = _("No course id was given!")
            
    template = loader.get_template("upload_img.html")
    return HttpResponse(template.render(c,request))	

#
# Edit image details
#
def edit_image(request):
    c = {}
    if not request.user.is_authenticated():
        c["message"] = _("You must be logged in to see this page")
        return redirect(login_view)

    if request.method == "POST":
        image = Image.objects.get(id=request.POST["id"])
        
        if 'delete' in request.POST:
            image.img.delete(save=True)
            image.delete()
            
        else:
            image.description = request.POST["description"]
            image.save()
            
        return redirect( reverse( project)+"?pid="+str(image.course.id))
    
    if 'id' not in request.GET:
        c["message"] = _("Image id not given.")

    image = Image.objects.get( id= request.GET["id"] )
    c["image"] = image
    
    template = loader.get_template("edit_img.html")
    context = RequestContext(request, c)
    return HttpResponse(template.render(context))	

#
# Upload a video file
#
def upload_video(request):
    c = {}
    if not request.user.is_authenticated():
        c["message"] = _("You must be logged in to see this page")
        return redirect(login_view)


    if 'pid' in request.POST:

        try:

            pid = request.POST["pid"]
            course = Course.objects.get(id=pid)
            vidfile = request.FILES["vid"]
            description = request.POST["description"]
        
            vid = Video(course=course, video=vidfile, description=description)
            vid.save()
            return HttpResponseRedirect(reverse('project')+"?pid=%s" % course.id)
        except Exception:
            c["message"] = _("Upload failed!")


    if 'pid' in request.GET:
        course = Course.objects.get(id=request.GET["pid"])
        c["course"] = course

    else:
        c["message"] = _("No course id was given!")
            
    template = loader.get_template("upload_vid.html")
    return HttpResponse(template.render(c,request))	
