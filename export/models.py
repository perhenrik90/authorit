from django.db import models
from authorit import settings
from cbuilder.models import Course, Slide

#
# Describes a build
#
class Build(models.Model):

    created = models.DateTimeField(auto_now_add=True)

    build_path = models.CharField(max_length=80)
    course = models.ForeignKey(Course)

    
# Describe one file in the build
class BuildFile(models.Model):

    filetype = models.CharField(max_length=40)
    file = models.FileField(upload_to="media/")
