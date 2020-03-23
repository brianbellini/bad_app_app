from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class App(models.Model):
    name = models.CharField(max_length=25)
    description = models.TextField(blank=True)
    slogan = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Comment(models.Model):
    words = models.TextField(blank=True)
    app = models.ForeignKey(App, on_delete=models.CASCADE)
