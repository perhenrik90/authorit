from django.template import loader, Template, Context
from django.shortcuts import render, redirect
from authorit import settings



class SCORM:

        # consctruct an exporter with a reference to a course
        def __init__(self, course, slides):
                self.course = course
                self.slides = slides
                self.path = settings.MEDIA_ROOT+'tmp/'

        def export_sco(self):
                c = {}
                c["course"] = self.course
                c["slides"] = self.slides
                
                context = Context(c)

                # setup main
                temp = loader.get_template("scorm/slides.html")
                f = open(self.path+"index.html","w")
                f.write(temp.render(context))
                f.close()

                temp = loader.get_template("scorm/bootstrap.css")
                f = open(self.path+"bootstrap.css","w")
                f.write(temp.render(context))
                f.close()

                temp = loader.get_template("scorm/bootstrap.js")
                f = open(self.path+"bootstrap.js","w")
                f.write(temp.render(context))
                f.close()
                                

                temp = loader.get_template("scorm/slidework.js")
                f = open(self.path+"slidework.js","w")
                f.write(temp.render(context))
                f.close()

                temp = loader.get_template("scorm/navbar.js")
                f = open(self.path+"navbar.js","w")
                f.write(temp.render(context))
                f.close()

                temp = loader.get_template("scorm/urltools.js")
                f = open(self.path+"urltools.js","w")
                f.write(temp.render(context))
                f.close()

                temp = loader.get_template("scorm/sdefault.css")
                f = open(self.path+"sdefault.css","w")
                f.write(temp.render(context))
                f.close()

                temp = loader.get_template("scorm/jquery-1.12.1.min.js")
                f = open(self.path+"jquery-1.12.1.min.js","w")
                f.write(temp.render(context))
                f.close()

                temp = loader.get_template("scorm/imsmanifest.xml")
                f = open(self.path+"imsmanifest.xml","w")
                f.write(temp.render(context))
                f.close()
                


                
                #slides = render(temp)
                # print(slides)


                
