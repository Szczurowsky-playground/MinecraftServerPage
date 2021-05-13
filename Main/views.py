from django.shortcuts import render, redirect
from .models import Post, User
from django.contrib import auth
from .forms import LoginValidate, RegisterValidate, SecurityValidate
from django.contrib.auth import authenticate, login

SERVER_NAME = 'Example server'


# Create your views here.
def home(request):
    posts = Post.objects.all()
    context = {
        'user': request.user,
        'SERVER_NAME': SERVER_NAME,
        'Title': 'Home',
        'post_list': posts,
    }
    return render(request, 'Main/index.html', context)


def register_view(request):
    context = {
        'SERVER_NAME': SERVER_NAME,
        'Title': 'Home',
    }
    if request.method == 'POST':
        form = RegisterValidate(request.POST)
        if form.is_valid():
            username = request.POST['username']
            email = request.POST['email']
            nickname = request.POST['nickname']
            password = request.POST['password']
            user = User.objects.create_user(username=username, email=email, nickname=nickname, password=password)
            user.save()
            login(request, user)
            return redirect('/')
        else:
            context = {
                'SERVER_NAME': SERVER_NAME,
                'Title': 'Home',
                'errors': form.errors.values(),
            }
    return render(request, 'Main/register.html', context)


def login_view(request):
    if request.user.is_authenticated:
        return redirect('/')
    context = {
        'SERVER_NAME': SERVER_NAME,
        'Title': 'Home',
    }
    if request.method == 'POST':
        form = LoginValidate(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                remember_me = request.POST.get('remember_me', False)
                if remember_me == "Yes":
                    request.session.set_expiry(3600 * 24 * 31)
                else:
                    request.session.set_expiry(3600 * 24)
                return redirect('/')
        else:
            context = {
                'SERVER_NAME': SERVER_NAME,
                'Title': 'Home',
                'errors': form.errors.values(),
            }
    return render(request, 'Main/login.html', context)


def logout(request):
    if request.user.is_authenticated:
        auth.logout(request)
    return redirect('/')


def security(request):
    if not request.user.is_authenticated:
        return redirect('/')
    send_user = User.objects.filter(username=request.user.username)
    context = {
        'SERVER_NAME': SERVER_NAME,
        'Title': 'Security',
        'user_sec': send_user,
    }
    if request.method == 'POST':
        form = SecurityValidate(request.POST)
        if form.is_valid():
            user = authenticate(request, username=request.user.username, password=request.POST['password'])
            if user is not None:
                if request.POST['email_new'] is not '' and request.POST['password_new'] is not '':
                    user.email = request.POST['email_new']
                    user.set_password(request.POST['password_new'])
                    user.save()
                    auth.logout(request)
                    return redirect('/login')
                if request.POST['email_new'] is not '' and request.POST['password_new'] is '':
                    user.email = request.POST['email_new']
                    user.save()
                    return redirect('/')
                if request.POST['email_new'] is '' and request.POST['password_new'] is not '':
                    user.set_password(request.POST['password_new'])
                    user.save()
                    auth.logout(request)
                    return redirect('/login')
        else:
            context = {
                'SERVER_NAME': SERVER_NAME,
                'Title': 'Security',
                'user_sec': send_user,
                'errors': form.errors.values(),
            }
    return render(request, 'Main/security.html', context)
