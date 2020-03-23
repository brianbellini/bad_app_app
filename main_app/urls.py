from django.urls import path
from . import views

urlpatterns = [
    #--------------------APPS-----------------------------
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('apps/', views.apps_index, name='index'),
    path('apps/<int:app_id>/', views.app_detail, name='detail'),
    path('apps/create/', views.app_create, name='app_create'),
    path('apps/<int:pk>/update/', views.app_update, name='app_update'),
    path('apps/<int:pk>/delete/', views.app_delete, name='app_delete'),

    #--------------------ACCOUNTS-----------------------------
    path('accounts/signup/', views.signup, name='signup'),
]