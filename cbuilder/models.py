from django.db import models
from django.contrib.auth.models import User

class CustomTheme(models.Model):

    title = models.CharField(max_length=80)
    created = models.DateTimeField(auto_now_add=True)
    css = models.FileField(upload_to="css/%Y")
    
    def __unicode__(self):
        return self.title
    
class Course(models.Model):

    title = models.CharField(max_length=80)
    code = models.CharField(max_length=80, unique=True)
    description = models.CharField(max_length=300)
    theme = models.ForeignKey(CustomTheme, null=True, blank=True)
    
    created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User)

    def __unicode__(self):
        return self.title


class Slide(models.Model):

    title = models.CharField(max_length=80)
    modified = models.DateTimeField(auto_now=True)

    html = models.CharField(max_length=5000)
    course = models.ForeignKey(Course)

    number = models.IntegerField()
    inMenu = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ('number', 'course')

    def __unicode__(self):
        return self.course.title +' '+str(self.number)+" : "+self.title

    
class Image(models.Model):

    img = models.FileField(upload_to="img/%Y")
    description = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    course = models.ForeignKey(Course)

    def __unicode__(self):
        return self.course.title + " " +self.created.strftime("%Y-%m-%d %H:%M:%S")
    
class Video(models.Model):

    description = models.CharField(max_length=250)
    videotype = models.CharField(max_length=16)
    video = models.FileField(upload_to="vid/%Y")
    created = models.DateTimeField(auto_now_add=True)
    course = models.ForeignKey(Course)   
    
    def __unicode__(self):
        return self.course.title + " " +self.created.strftime("%Y-%m-%d %H:%M:%S")
