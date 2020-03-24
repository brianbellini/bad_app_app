from django.contrib import admin
from .models import App, Comment, Vote

# Register your models here.
admin.site.register(App)
admin.site.register(Comment)
admin.site.register(Vote)

