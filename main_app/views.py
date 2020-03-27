from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django import forms
from .forms import CommentForm
import uuid
import boto3
S3_BASE_URL = 'HTTPS://s3-us-east-2.amazonaws.com/'
BUCKET = 'badappapp'

from .models import Vote, App, Comment, Photo
from .forms import SignupForm
from random import randint

# Create your views here.
#--------------------APPS-----------------------------
def landing(request):
    apps = App.objects.all()
    return render(request, 'landing.html', {'apps': apps})

@login_required
def home(request):
    # App of the day - figure out how to find random
    ordered_app = App.objects.all().order_by('-id')
    total = ordered_app[0].id
    random_app = None
    while not random_app:
        random = randint(1, total)
        if App.objects.filter(id=random).first():
            random_app = App.objects.get(id=random)
        else: 
            random
    pop_apps = App.objects.all().order_by('net_votes')[:3]
    my_apps = App.objects.filter(user=request.user)
    return render(request, 'home.html', {'my_apps': my_apps, 'pop_apps': pop_apps, 'random_app': random_app})

def about(request):
    return render(request, 'about.html')

def apps_index(request):
    ordered_app = App.objects.all().order_by('-id')
    total = ordered_app[0].id
    random_app = None
    while not random_app:
        random = randint(1, total)
        if App.objects.filter(id=random).first():
            random_app = App.objects.get(id=random)
        else: 
            random
    pop_apps = App.objects.all().order_by('net_votes')[:3]
    apps = App.objects.all()
    return render(request, 'apps/index.html', {'apps': apps, 'pop_apps': pop_apps, 'random_app': random_app})

@login_required
def app_detail(request, app_id):
    app = App.objects.get(id=app_id)
    comments = Comment.objects.filter(app = app_id).order_by('-id')
    comment_form = CommentForm()
    votes = Vote.objects.filter(user = request.user.id)
    voted = False
    has_voted = False
    vote_value = None
    for vote in votes:
        if vote.app.id == app_id:
            voted = True
            vote_value = vote.value
            break
        else:
            voted = False
    
    return render(request, 'apps/detail.html', {
        'app': app,
        'comments': comments,
        'voted': voted,
        'vote_value': vote_value,
        'comment_form': comment_form,
    })

@login_required
def app_good(request, app_id):
    app = App.objects.get(id=app_id)
    app.good_vote()
    vote = Vote()
    vote.app = app
    vote.user = request.user
    vote.value = 1
    vote.save()

    return redirect("detail", app_id=app_id)

@login_required
def app_bad(request, app_id):
    app = App.objects.get(id=app_id)
    app.bad_vote()
    vote = Vote()
    vote.app = app
    vote.user = request.user
    vote.value = -1
    vote.save()

    return redirect("detail", app_id=app_id)

@login_required
def remove_good(request, app_id):
    app = App.objects.get(id=app_id)
    app.bad_vote()
    vote = Vote.objects.filter(app=app_id, user=request.user.id)
    vote.delete()

    return redirect("detail", app_id=app_id)

@login_required
def remove_bad(request, app_id):
    app = App.objects.get(id=app_id)
    app.good_vote()
    vote = Vote.objects.filter(app=app_id, user=request.user.id)
    vote.delete()

    return redirect("detail", app_id=app_id)



class AppCreate(LoginRequiredMixin, CreateView):
    model = App
    fields = ['name', 'description', 'slogan', 'developer', 'tag']
    success_url = '/home/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class AppUpdate(LoginRequiredMixin, UpdateView):
    model = App
    fields = ['description', 'slogan', 'developer', 'tag']


class AppDelete(LoginRequiredMixin, DeleteView):
    model = App
    success_url = '/home/'


#--------------------COMMENTS-----------------------------
@login_required
def add_comment(request, app_id):
    form = CommentForm(request.POST)
    if form.is_valid():
        new_comment = form.save(commit=False)
        new_comment.app_id = app_id
        new_comment.user_id = request.user.id
        new_comment.save()
    return redirect('detail', app_id=app_id)

@login_required
def delete_comment(request, app_id, comment_id):
    comment = Comment.objects.get(id=comment_id)
    comment.delete()
    return redirect('detail', app_id=app_id)


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

#--------------------PHOTOS-----------------------------
@login_required
def add_photo(request, app_id):
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            url = f"{S3_BASE_URL}{BUCKET}/{key}"
            photo = Photo(url=url, app_id=app_id)
            photo.save()
        except:
            print('An error occured uploading file to S3')
    return redirect('detail', app_id=app_id)

