from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.contrib import messages
from .models import *
from django.conf import settings


# Create your views here.
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def home(request):
    return render(request, 'home.html')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def login_page(request):
    if request.method == 'POST':
        usrname = request.POST['username']
        password = request.POST['password']

        if User.objects.filter(email=usrname):
            requesting_user = requesting_user = User.objects.get(email=usrname)
            if authenticate(username=requesting_user.username, password=password):
                messages.success(request, 'Logged in successfully')
                login(request, requesting_user)
                return HttpResponseRedirect('/')
            else:
                messages.error(request, 'Wrong password !')
                return HttpResponseRedirect('/loginuser')
        else:
            messages.error(request, 'No user found ! Register first')
            return HttpResponseRedirect('/registeruser')

        
    return render(request, 'LoginPage.html')

def registration(request):
    if request.method == 'POST' and request.FILES['pic']:
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        password = request.POST['password']
        pic = request.FILES['pic']

        if fname == '' or fname == ' ':
            messages.error(request, 'Enter first name please!')
            return HttpResponseRedirect('/registeruser')
        if lname == '' or lname == ' ':
            messages.error(request, 'Enter last name please!')
            return HttpResponseRedirect('/registeruser')
        if email == '' or email == ' ':
            messages.error(request, 'Enter Email-ID please!')
            return HttpResponseRedirect('/registeruser')
        if password == '' or password == ' ':
            messages.error(request, 'Enter Password please!')
            return HttpResponseRedirect('/registeruser')
        if len(password) < 8:
            messages.error(request, 'Password must contain atleast 8 characters')
            return HttpResponseRedirect('/registeruser')
        if not any(x.islower() for x in password):
            messages.error(request, 'Password must contain atleast 1 lowercase character')
            return HttpResponseRedirect('/registeruser')
        if not any(x.isupper() for x in password):
            messages.error(request, 'Password must contain atleast 1 uppercase character')
            return HttpResponseRedirect('/registeruser')
        if not any(x.isdigit() for x in password):
            messages.error(request, 'Password must contain atleast 1 digit')
            return HttpResponseRedirect('/registeruser')
        else:
            if User.objects.filter(email=email):
                messages.error(request, 'Email-ID already used.')
                return HttpResponseRedirect('/')
                
            user = User.objects.create_user(fname, email, password)
            user.first_name = fname
            user.last_name = lname
            user.save()

            appuser = AppUser(user=user, profile_pic=pic)
            appuser.save()
            messages.success(request, 'Registered successfully')
            return HttpResponseRedirect('/')


    return render(request, 'registration.html')


@cache_control(no_cache=True, must_revalidade=True, no_store=True)
@login_required(login_url='loginuser')
def main_page(request):
    current_user = AppUser.objects.get(user=request.user)
    if request.method == 'POST':
        heading = request.POST['heading']
        data = request.POST['data']
        if request.FILES.get('blog_img'):
            img = request.FILES['blog_img']
            blog = Blogs(user=current_user, heading=heading, data=data, picture=img)
        else:
            blog = Blogs(user=current_user, heading=heading, data=data)
    
        blog.save()
        messages.success(request, 'Blog posted successfully.')
        return HttpResponseRedirect('/main')



    data = list(Blogs.objects.all())
    usr = list(AppUser.objects.all())
    # print(usr[i].profile_pic)
    # print('name', data[0].user.user.first_name)
    return render(request, 'main.html', {'data' : data, 'user' : usr})

@cache_control(no_cache=True, must_revalidade=True, no_store=True)
@login_required(login_url='loginuser')
def profile(request):
    appuser = AppUser.objects.get(user=request.user)
    blogs_count = len(list(Blogs.objects.filter(user=appuser)))
    return render(request, 'profile.html', {'appuser' : appuser, 'blogs' : blogs_count})

@cache_control(no_cache=True, must_revalidade=True, no_store=True)
@login_required(login_url='loginuser')
def requested_user(request, user_id):
    required = AppUser.objects.get(id=user_id)
    blogs_count = len(list(Blogs.objects.filter(user=required)))
    return render(request, 'request_profile.html', {'required' : required, 'blogs' : blogs_count})
    
@cache_control(no_cache=True, must_revalidade=True, no_store=True)
def logoutuser(request):
    logout(request)
    messages.success(request, 'Logged out successfully')
    return HttpResponseRedirect('/')