from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django import forms

from .models import App, Comment
from .forms import SignupForm
from random import randint

# Create your views here.
#--------------------APPS-----------------------------
def landing(request):
    apps = App.objects.all()
    return render(request, 'landing.html', {'apps': apps})

def home(request):
    # App of the day - figure out how to find random
    total = len(App.objects.all())
    random = randint(1, total)
    random_app = App.objects.get(id=random)
    pop_apps = App.objects.all().order_by('net_votes')[:3]
    my_apps = App.objects.filter(user=request.user)
    return render(request, 'home.html', {'my_apps': my_apps, 'pop_apps': pop_apps, 'random_app': random_app})

def about(request):
    return render(request, 'about.html')

def apps_index(request):
    apps = App.objects.all()
    return render(request, 'apps/index.html', {'apps': apps})

def app_detail(request, app_id):
    app = App.objects.get(id=app_id)
    comments = Comment.objects.filter(app = app_id)

    return render(request, 'apps/detail.html', {
        'app': app,
        'comments': comments,
    })

@login_required
def app_create(request):
    return HttpResponse('CREATE NEW APP')

@login_required
def app_update(request):
    return HttpResponse('UPDATE APP')

@login_required
def app_delete(request):
    return HttpResponse('DELETE APP')

#--------------------COMMENTS-----------------------------
@login_required
def add_comment(request, app_id):
    form = CommentForm(request.POST)
    if form.is_valid():
        new_comment = form.save(commit=false)
        new_comment.app_id = app_id
        new_comment.save()
    return redirect('detal', app_id=app_id)

class CommentDelete(LoginRequiredMixin, DeleteView):
  model = Comment
  success_url = '/apps/'

#--------------------ACCOUNTS-----------------------------
def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
        else:
            error_message = 'Invalid sign up - try again'
    form = SignupForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)
