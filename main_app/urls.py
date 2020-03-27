from django.urls import path
from . import views

urlpatterns = [
    #--------------------APPS-----------------------------
    path('', views.apps_index, name='index'),
    path('home/', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('apps/', views.apps_index, name='index'),
    path('apps/<int:app_id>/', views.app_detail, name='detail'),
    path('apps/create/', views.AppCreate.as_view(), name='app_create'),
    path('apps/<int:pk>/update/', views.AppUpdate.as_view(), name='app_update'),
    path('apps/<int:pk>/delete/', views.AppDelete.as_view(), name='app_delete'),
    path('apps/<int:app_id>/good/', views.app_good, name='good'),
    path('apps/<int:app_id>/bad/', views.app_bad, name='bad'),
    path('apps/<int:app_id>/remove_good/', views.remove_good, name='remove_good'),
    path('apps/<int:app_id>/remove_bad/', views.remove_bad, name='remove_bad'),
    path('apps/<int:app_id>/add_comment/', views.add_comment, name='add_comment'),
    path('apps/<int:app_id>/delete_comment/<int:comment_id>/', views.delete_comment, name='delete_comment'),

    #--------------------ACCOUNTS-----------------------------
    path('accounts/signup/', views.signup, name='signup'),

    #--------------------PHOTOS-----------------------------
    path('apps/<int:app_id>/add_photo/', views.add_photo, name='add_photo'),

]