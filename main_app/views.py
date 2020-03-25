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
    total = len(App.objects.all())
    print(f"total: {total}")
    random = randint(1, total)
    print(f"random: {random}")
    random_app = App.objects.get(id=random)
    pop_apps = App.objects.all().order_by('net_votes')[:3]
    apps = App.objects.all()
    return render(request, 'apps/index.html', {'apps': apps, 'pop_apps': pop_apps, 'random_app': random_app})

def app_detail(request, app_id):
    app = App.objects.get(id=app_id)
    comments = Comment.objects.filter(app = app_id)

    return render(request, 'apps/detail.html', {
        'app': app,
        'comments': comments,
    })

class AppCreate(LoginRequiredMixin, CreateView):
    model = App
    fields = ['name', 'description', 'slogan', 'group', 'tag']
    success_url = '/home/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class AppUpdate(LoginRequiredMixin, UpdateView):
    model = App
    fields = ['description', 'slogan', 'group', 'tag']


class AppDelete(LoginRequiredMixin, DeleteView):
    model = App


#--------------------COMMENTS-----------------------------
@login_required
def add_comment(request, app_id):
    form = CommentForm(request.POST)
    if form.is_valid():
        new_comment = form.save(commit=False)
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
