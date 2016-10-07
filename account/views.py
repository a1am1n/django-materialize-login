# -*- coding: utf-8 -*-
from django.http import Http404
from django.shortcuts import render
from account.models import *
from django.http import HttpResponseRedirect, HttpResponse
from account.forms import *
from django.contrib.auth import *

from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,authenticate
from django.views.generic import TemplateView



#Login View
def login_v(request):
    msg=''
    form=LoginForm()
    print (request)
    
    print (request.user)
    if request.user.is_authenticated():
        return HttpResponseRedirect('/admin/')
        
    else:
        if request.method=="POST":
            form=LoginForm(request.POST)
            
        if form.is_valid():
            userid=form.cleaned_data['email']
            password=form.cleaned_data['password']
            auth_user=authenticate(username=userid,password=password)
            
        # If user exist and is active. Authenticate and redirect to /admin/
        if auth_user is not None and auth_user.is_active:
            login(request,auth_user)
            return HttpResponseRedirect('/admin/')
          
        else:
            msg='Wrong password'
        
        form=LoginForm()
        auth_user=authenticate(username=userid,password=password)
        if auth_user is not None:
            login(request,auth_user)
            return HttpResponseRedirect('/admin/')
        
        else:
            msg='Wrong password'

    return render(request, 'login.html', locals())
  
  
#The Signup  view
class SignUp(TemplateView):
  def post(self,request, *args,**kwargs):
      msg=''
      form = SignUpForm(request.POST)
      password=None
      if form.is_valid():
          email=form.cleaned_data['email']
          password=form.cleaned_data['password']
          confirm_password=form.cleaned_data['confirm_password']
      if (password!=confirm_password):
          msg='Passwords dot not match!'
          ctx={'form':form,'msg':msg}
          return render(request,self.template_name,locals())
      new_usp=None

      try:
          # We create the user
          new_usr=User.objects.create_user(username=email, email=email, password=password)
          new_usp=UserProfile(user=new_usr,organization=new_org)
      except: # If user is created. Then we notificate
          msg='account with email ' + email +' alreay created!'
          ctx={'form':form,'msg':msg}
          return render(request,self.template_name,locals())

      new_usp.save()
      new_usr.save()

      new_user = authenticate(username=email,password=password)
      
      if new_user is not None :
          login(request,new_user)
          return HttpResponseRedirect('/admin/')
      else:
          msg='Wrong info'
          form = SignUpForm()
          ctx={'form':form,'msg':msg}
          return render(request,self.template_name,locals())

  def get(self, request, *args, **kwargs):
      print (self)
      msg=''
      form = SignUpForm()
      if request.user.is_authenticated():
          return redirect('/admin/')
      
      return render(request,self.template_name,locals())
