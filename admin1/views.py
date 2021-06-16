from django.http.response import JsonResponse
from django.shortcuts import render,redirect
from django.views.generic import View,TemplateView,ListView
from django.contrib.auth import authenticate, login
# from django.contrib.auth.forms import AuthenticationForm
from user.forms import UserRegisterForm,AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.contrib.auth import logout
from user.models import *

# Create your views here.
class AdLoginView(View):

    def get(self,request):
        if self.request.session.has_key('adminkey'):
            return redirect('home')
        else:
            return render(request, 'admintemplates/login.html',{'form':AuthenticationForm})
    
    def post(self,request):
        form = AuthenticationForm(request, data = request.POST)
        if form.is_valid():
            user = authenticate(request, username = form.cleaned_data.get('username'), password = form.cleaned_data.get('password'))
            if user.is_superuser  == True:
                form.confirm_login_allowed(user)
                login(request,user)
                self.request.session['adminkey']='admin'
                return redirect('home') 
            else:
                messages.info(request,'sorry, that login was invalid since you are not an admin.')
                return redirect('AdLoginView')
              
        else:
            messages.info(request,'sorry, that login was invalid. Please try again.')
            return redirect('/admin/')
       
def home(request):
    if request.session.has_key('adminkey'):
        return render(request, 'admintemplates/index.html')
    else:
        return redirect('AdLoginView')

def user_list(request):
    if request.session.has_key('adminkey'):
        users = User_Profile.objects.exclude(is_superuser=True)
        context = {'users':users}
        return render(request,'admintemplates/usertable.html',context)
    else:
        return redirect('AdLoginView')
def user_block(request, id):
    if request.session.has_key('adminkey'):
        user = User_Profile.objects.get(id=id)
        print(user)
        if user.is_active == True:
            user.is_active = False
            
        else:
            user.is_active = True
        user.save()
        return JsonResponse('true', safe=False)
    else:
        return redirect('AdLoginView')

class AdLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('/admin/')
    
