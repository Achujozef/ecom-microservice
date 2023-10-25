from django.urls import path
from . import views
app_name = 'wallet'
urlpatterns = [
    path('wallet_balance/', views.wallet_balance_view, name='wallet_balance'),
    path('deposit/', views.deposit_view, name='deposit'),
    path('withdraw/', views.withdraw_view, name='withdraw'),
    path('transfer/', views.transfer_view, name='transfer'),
    path('wallet_payment/', views.wallet_payment_view, name='wallet_payment'),
    # Other URL patterns for your gateway service
]
