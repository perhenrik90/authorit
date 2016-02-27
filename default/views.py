from django.shortcuts import render
from django.shortcuts import render, redirect
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse
from django.template import RequestContext, loader, Template, Context
from django.http import HttpResponse

from cbuilder.models import Course


def overview(request):

    c = {}

    c["courses"] = Course.objects.filter(owner=request.user)
    
    template = loader.get_template("overview.html")
    context = RequestContext(request, c)
    return HttpResponse(template.render(context))
