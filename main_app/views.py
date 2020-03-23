from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm


# Create your views here.
#--------------------APPS-----------------------------
def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def apps_index(request):
    return HttpResponse('INDEX')

def app_detail(request):
    return HttpResponse('DETAIL')

def app_create(request):
    return HttpResponse('CREATE NEW APP')

def app_update(request):
    return HttpResponse('UPDATE APP')

def app_delete(request):
    return HttpResponse('DELETE APP')

#--------------------ACCOUNTS-----------------------------

def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
        else:
            error_message = 'Invalid sign up - try again'
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)