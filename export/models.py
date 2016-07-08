# -*- coding: latin-1 -*-
from django.db import models
from django.utils.encoding import smart_str
from authorit import settings
from cbuilder.models import Course, Slide

#
# Describes a build
#
class Build(models.Model):

    created = models.DateTimeField(auto_now_add=True)

    build_path = models.CharField(max_length=80)
    course = models.ForeignKey(Course)

    def __unicode__(self):
        return self.created

    def __str__(self):
        return self.course.title.encode('utf8')
    
# Describe one file in the build
class BuildFile(models.Model):

    filetype = models.CharField(max_length=40)
    file = models.FileField(upload_to="media/")
