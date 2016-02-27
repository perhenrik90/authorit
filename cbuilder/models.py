from django.db import models
from django.contrib.auth.models import User

class Course(models.Model):

    title = models.CharField(max_length=26)
    description = models.CharField(max_length=300)

    created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User)


class Slide(models.Model):

    title = models.CharField(max_length=26)
    modified = models.DateTimeField(auto_now=True)

    
    html = models.CharField(max_length=1500)
    course = models.ForeignKey(Course)

