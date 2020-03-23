from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Tag(models.Model):
    name = models.CharField(max_length=25)

    def __str__(self):
        return self.name

class App(models.Model):
    name = models.CharField(max_length=25)
    description = models.TextField(blank=True)
    slogan = models.CharField(max_length=50)
    group = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tag = models.ManyToManyField(Tag)

    def __str__(self):
        return self.name

class Comment(models.Model):
    words = models.TextField(blank=True)
    app = models.ForeignKey(App, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
class Vote(models.Model):
    app = models.ForeignKey(App, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)