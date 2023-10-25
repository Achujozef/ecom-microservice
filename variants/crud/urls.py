from django.urls import path
from . import views 

urlpatterns = [
   path('create_variant/', views.create_variant, name='create_variant'),
   path('update_variant/<int:variant_id>/', views.update_or_delete_variant, name='update_or_delete_variant'),
   path('get_variants/', views.get_variants_by_product, name='get_variants_by_product'),
]
