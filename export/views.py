from django.shortcuts import render, redirect
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse
from django.template import RequestContext, loader, Template, Context
from django.http import HttpResponse


def preview(request):

    c = {}

    template = loader.get_template("slides.html")
    context = RequestContext(request, c)
    return HttpResponse(template.render(context))