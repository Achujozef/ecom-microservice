from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.ADD, name='add_product'),
    path('update_product/<int:id>/', views.update_product, name='update_product'),
    path('get_product/', views.get_product_with_images, name='get_product_with_images'),
    path('get_product/<int:product_id>/', views.get_product_with_images, name='get_product_with_images'),
    path('delete/<int:product_id>/', views.delete_product, name='delete_product'),
    path('filter_products/', views.filter_products, name='filter_products'),
    path('get_products_by_category/<int:category>/', views.get_products_by_category, name='products_by_category'),
]
