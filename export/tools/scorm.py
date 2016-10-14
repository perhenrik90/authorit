# -*- coding: utf-8 -*-
from django.template import loader, Template, Context
from django.shortcuts import render, redirect
from authorit import settings

class SCORM:

        # consctruct an exporter with a reference to a course
        def __init__(self, course):
                self.course = course
                self.path = settings.MEDIA_ROOT+'tmp/'
                

        def export_sco(self):
                course = self.course
                c = {}
                c["course"] = course
                temp = loader.get_template("scorm/slides.html")
                slides = render(temp)
                print(slides)
