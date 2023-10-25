from django.urls import path
from . import views

urlpatterns = [
    path('add_product', views.add_product, name='add_product'),
    path('edit_product/<int:id>/', views.edit_product, name='edit_product'),
    path('admin_product_page/', views.admin_product_page, name='admin_product_page'),
    path('delete_product/<int:product_id>/', views.delete_product, name='delete_product'),
    path('shop/', views.shop, name='shop'),
    path('shop/<int:id>/', views.shop, name='shop'),
    path('add_variant_prod/<int:product_id>/', views.add_variant_prod, name='add_variant_prod'),
    path('edit_variants/<int:product_id>/', views.edit_variants, name='edit_variants'),
    path('shopsingle/', views.shopsingle, name='shopsingle'),


]