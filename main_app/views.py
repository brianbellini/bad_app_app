from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import App, Comment
from django.contrib.auth.models import User


# Create your views here.
#--------------------APPS-----------------------------
def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def apps_index(request):
    apps = App.objects.all()
    return render(request, 'apps/index.html', {'apps': apps})

def app_detail(request, app_id):
    app = App.objects.get(id=app_id)
    comments = Comment.objects.filter(app_id)

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
# def signup(request):
#     error_message = ''
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             return redirect('index')
#         else:
#             error_message = 'Invalid sign up - try again'
#     form = UserCreationForm()
#     context = {'form': form, 'error_message': error_message}
#     return render(request, 'registration/signup.html', context)

class RegisterForm(UserCreationForm):
    email = forms.EmailField(label = 'Email')
    first_name = forms.CharField(label = 'First name')
    last_name = forms.CharField(label= 'Last name')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email',)

def save(self, commit=True):
    user = super(RegisterForm, self).save(commit-False)
    user.first_name = first_name
    user.last_name = last_name
    user.email = self.cleaned_data["email"]
    if commit:
        user.save()
    return user