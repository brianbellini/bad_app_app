from django.contrib import admin
from .models import App, Comment, Tag, Vote

# Register your models here.
admin.site.register(App)
admin.site.register(Comment)
admin.site.register(Tag)
admin.site.register(Vote)

