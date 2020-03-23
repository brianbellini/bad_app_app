from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class App(models.Model):
    name = models.CharField(max_length=25)
    description = models.CharField(max_length=250)

    def __str__(self):
        return self.name

class Comment(models.Model):
    words = models.TextField(blank=True)
    
