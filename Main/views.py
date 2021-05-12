from django.shortcuts import render, redirect
from .models import Post
from django.contrib import auth
from .forms import LoginValidate
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
