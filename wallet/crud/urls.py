from django.urls import path
from . import views

urlpatterns = [
    path('deposit/', views.deposit_view, name='deposit_wallet'),
    path('withdraw/', views.withdraw_view, name='withdraw_wallet'),
    path('transfer/', views.transfer_view, name='transfer_wallet'),
    path('payment/', views.payment_view, name='payment_wallet'),
    path('get_wallet_balance/', views.get_wallet_balance, name='get_wallet_balance'),
    # Other URL patterns for your wallet service
]
