# -*- coding: utf-8 -*-
import os
import codecs
import re
import zipfile
from io import StringIO
from io import BytesIO
from django.core.files import File

from django.template import loader, Template, Context
from django.shortcuts import render, redirect
from django.core import serializers
from django.core.files.base import ContentFile

from authorit import settings
import sys

from cbuilder.models import Course, Slide, Image

class SCORM_Export:

        # consctruct an exporter with a reference to a course
        def __init__(self, course, slides, images,videos):
                self.course = course
                self.slides = slides
                self.images = images
                self.videos = videos
                
                if not os.path.isdir(settings.MEDIA_ROOT):
                        os.makedirs(settings.MEDIA_ROOT)

                if not os.path.isdir(settings.MEDIA_ROOT+"tmp/"):
                        os.makedirs(settings.MEDIA_ROOT+"tmp/")

                if not os.path.isdir(settings.MEDIA_ROOT+"scorm/"):
                        os.makedirs(settings.MEDIA_ROOT+"scorm/")

                if not os.path.isdir(settings.MEDIA_ROOT+"tmp/"+course.code):
                        os.makedirs(settings.MEDIA_ROOT+"tmp/"+course.code)

                if not os.path.isdir(settings.MEDIA_ROOT+"tmp/"+course.code+"/img/"):
                        os.makedirs(settings.MEDIA_ROOT+"tmp/"+course.code+"/img/")
                        
                      
                self.path = settings.MEDIA_ROOT+'tmp/'+course.code+"/"
                self.img_path = settings.MEDIA_ROOT+"tmp/"+course.code+"/img/"
                self.scorm_path = settings.MEDIA_ROOT+'scorm/'+course.code+".zip"


        # export files to tmp direcotry
        def export_scorm(self):
                c = {}
                c["course"] = self.course
                c["slides"] = self.slides

                context = Context(c)
                z = zipfile.ZipFile(self.scorm_path,'w')
                
                # setup main
                temp = loader.get_template("scorm/slides.html")
                f = codecs.open(self.path+"index.html","w", "utf-8")
                rended = temp.render(context)
                rended = re.sub("http://.*?/","",rended);

                f.write(rended)
                f.close()
                z.write(self.path+"index.html", arcname="index.html")

                temp = loader.get_template("scorm/bootstrap.css")
                f = open(self.path+"bootstrap.css","w")
                f.write(temp.render(context))
                f.close()
                z.write(self.path+"bootstrap.css", arcname="bootstrap.css")

                z.write(settings.SCORM_ROOT+"glyphicons-halflings-regular.eot", arcname="glyphicons-halflings-regular.eot")
                z.write(settings.SCORM_ROOT+"glyphicons-halflings-regular.ttf", arcname="glyphicons-halflings-regular.ttf")
                z.write(settings.SCORM_ROOT+"glyphicons-halflings-regular.woff", arcname="glyphicons-halflings-regular.woff")
                z.write(settings.SCORM_ROOT+"glyphicons-halflings-regular.woff2", arcname="glyphicons-halflings-regular.woff2")
                
                temp = loader.get_template("scorm/bootstrap.js")
                f = open(self.path+"bootstrap.js","w")
                f.write(temp.render(context))
                f.close()
                z.write(self.path+"bootstrap.js", arcname="bootstrap.js")


                temp = loader.get_template("scorm/slidework.js")
                f = open(self.path+"slidework.js","w")
                f.write(temp.render(context))
                f.close()
                z.write(self.path+"slidework.js", arcname="slidework.js")

                temp = loader.get_template("scorm/quiztool.js")
                f = open(self.path+"quiztool.js","w")
                f.write(temp.render(context))
                f.close()
                z.write(self.path+"quiztool.js", arcname="quiztool.js")

                temp = loader.get_template("scorm/welltool.js")
                f = open(self.path+"welltool.js","w")
                f.write(temp.render(context))
                f.close()
                z.write(self.path+"welltool.js", arcname="welltool.js")
                
                temp = loader.get_template("scorm/navbar.js")
                f = open(self.path+"navbar.js","w")
                f.write(temp.render(context))
                f.close()
                z.write(self.path+"navbar.js", arcname="navbar.js")

                temp = loader.get_template("scorm/urltools.js")
                f = open(self.path+"urltools.js","w")
                f.write(temp.render(context))
                f.close()
                z.write(self.path+"urltools.js", arcname="urltools.js")

                temp = loader.get_template("scorm/sdefault.css")
                f = open(self.path+"sdefault.css","w")
                f.write(temp.render(context))
                f.close()
                z.write(self.path+"sdefault.css", arcname="sdefault.css")
                

                temp = loader.get_template("scorm/jquery-1.12.1.min.js")
                f = open(self.path+"jquery-1.12.1.min.js","w")
                f.write(temp.render(context))
                f.close()
                z.write(self.path+"jquery-1.12.1.min.js", arcname="jquery-1.12.1.min.js")

                temp = loader.get_template("scorm/imsmanifest.xml")
                f = open(self.path+"imsmanifest.xml","w")
                f.write(temp.render(context))
                f.close()
                z.write(self.path+"imsmanifest.xml", arcname="imsmanifest.xml")

		temp = loader.get_template("scorm/SCORM_API_wrapper.js")
                f = open(self.path+"SCORM_API_wrapper.js","w")
                f.write(temp.render(context))
                f.close()
                z.write(self.path+"SCORM_API_wrapper.js", arcname="SCORM_API_wrapper.js")

                # add images
                for img in self.images:
                        full_p = settings.MEDIA_ROOT+str(img.img)
                        relative = 'media/'+img.img.name
                        z.write(full_p, arcname=relative)

                # add videos
                for video in self.videos:
                        full_p = settings.MEDIA_ROOT+str(img.img)
                        relative = 'media/'+img.img.name
                        z.write(full_p, arcname=relative)

                # add custom css
                if self.course.theme:
                        full_p = settings.MEDIA_ROOT+str(self.course.theme.css)
                        relative = 'media/'+self.course.theme.css.name
                        z.write(full_p, arcname=relative)
                        
                ######################################################
                # Export authorit / django xml
                # used to export courses to other authorit instances
                ######################################################
                        
                # add django objects for exporting issues
                course_xml = serializers.serialize("xml", [self.course])
                f = open(self.path+"authorit_course.xml","w")
                f.write(course_xml)
                f.close()
                z.write(self.path+"authorit_course.xml", arcname="authorit/authorit_course.xml")

                slides_xml = serializers.serialize("xml", self.slides)
                f = open(self.path+"authorit_slides.xml","w")
                f.write(slides_xml)
                f.close()
                z.write(self.path+"authorit_slides.xml", arcname="authorit/authorit_slides.xml")                        

                # close zip
                z.close()
                
		return self.scorm_path


#
# Import a SCORM packages exported with authorit
#

def SCORM_Import(user, new_code, ffile):

        if not os.path.isdir(settings.MEDIA_ROOT+"tmpupload/"):
                os.makedirs(settings.MEDIA_ROOT+"tmpupload/")
        upload_path = settings.MEDIA_ROOT+"tmpupload/"
        
        z = zipfile.ZipFile(ffile)
        
        # load course xml and create a new course instance
        course_xml = str(z.read('authorit/authorit_course.xml'))

        imported_course = None
        for course in serializers.deserialize("xml", course_xml, ignorenonexistent=True):
                course.object.code = new_code
                course.object.id = None 
                course.object.owner = user
                course.object.save()
                imported_course = course.object

        # import image mediafiles and store changes in a dictionary
        old_new_path = {}
        files2 = z.extractall(settings.MEDIA_ROOT+"/tmpupload")

        print files2
        files = z.namelist()
        i = 0
        for path in files:

                if 'media/img/' in path:

                        data = open(settings.MEDIA_ROOT+"tmpupload/"+path,'r')
                        data = File(data)
                        
                        nimage = Image(img=data)
                        nimage.course = imported_course
                        nimage.save()

                        old_new_path[path] = str(settings.MEDIA_URL)+str(nimage.img.name)
                        i += 1

        
        # import the slides and them to the new course instance
        slides_xml = str(z.read('authorit/authorit_slides.xml'))
        for slide in serializers.deserialize("xml", slides_xml, ignorenonexistent=True):

                # for all slides, update new path for images based on dictionary
                for old_path in old_new_path:
                        slide.object.html = slide.object.html.replace(old_path, old_new_path[old_path])

                # replace absolute url with server relative
                slide.object.html = re.sub("https://.*/media","/media/",slide.object.html)
                slide.object.html = re.sub("http://.*/media","/media/",slide.object.html)
                
                # clear id
                slide.object.id = None
                slide.object.course = imported_course
                slide.object.save()
        
        return imported_course
                


                
