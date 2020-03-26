from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from django.contrib.auth.models import User
from .models import Comment


class SignupForm(UserCreationForm):
  class Meta:
    model = User
    fields = [
      'username',
      'email',
      'first_name',
      'last_name',
      'password1',
      'password2',
    ]

class CommentForm(ModelForm):
  class Meta:
    model = Comment
    fields = ['words']