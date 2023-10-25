from django.urls import path
from . import views

urlpatterns = [
    path('', views.base_file, name='base_file'),
    path('adminbannerlist/', views.adminbannerlist, name='adminbannerlist'),
    path('deletebanner/', views.deletebanner, name='deletebanner'),
    path('adminaddbanner/', views.adminaddbanner, name='adminaddbanner'),

]
app_name = 'banner'