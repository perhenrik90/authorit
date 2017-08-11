from django.shortcuts import render
from django.shortcuts import render, redirect
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse
from django.template import RequestContext, loader, Template, Context
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout

from cbuilder.models import Course


def login_view(request):
    user = request.user
    c = {}
    if user.is_authenticated():
        return dashboard(request)

    if request.method == "POST":
        us = request.POST["username"] 
        pa = request.POST["pass"]         

        usr = authenticate(username=us, password=pa)
        if(usr is not None):
            # check if the user is activated
            if(usr.is_active):
                login(request, usr)
                return redirect(dashboard)
            else:
               c["message"] = _("Your user is suspended.")

        # mark that the user has tried to login
        c["not_authenticated"] = 1
        
    template = loader.get_template('login.html')
    context = RequestContext(request, c)
    return HttpResponse(template.render(c, request))

#
# The users dashboard
#
def dashboard(request):

    c = {}
    if not request.user.is_authenticated():
        c["message"] = _("You must be logged in to see this page")
        return redirect(login_view)

    c["courses"] = Course.objects.filter(owner=request.user)
    
    template = loader.get_template("overview.html")
    context = RequestContext(request, c)
    return HttpResponse(template.render(c, request))
