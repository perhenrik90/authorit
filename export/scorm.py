# -*- coding: utf-8 -*-
import os
import codecs
import zipfile

from django.template import loader, Template, Context
from django.shortcuts import render, redirect
from authorit import settings
import sys


class SCORM:

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
                f.write(temp.render(context))
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
                        z.write(full_p)

                # add videos
                for video in self.videos:
                        full_p = settings.MEDIA_ROOT+str(video.video)
                        z.write(full_p)
                                
                z.close()
                
		return self.scorm_path
                #slides = render(temp)
                # print(slides)


                
