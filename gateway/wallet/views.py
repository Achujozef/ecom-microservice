import requests
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from decimal import Decimal
from authentication.models import UserDetail
# Import your Wallet and Transaction models if needed

  # Import the UserDetail model

def wallet_balance_view(request):
    if 'username' in request.session:
        # Retrieve the user's session data (e.g., username)
        username = request.session['username']
        
        # Retrieve the user_id from the UserDetail model
        try:
            user = UserDetail.objects.get(uname=username)
            user_id = user.id  # Assuming that the 'id' field in UserDetail is the user_id
        except UserDetail.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=500)

        # Send a request to the wallet service to get wallet balance
        wallet_service_url = 'http://localhost:8004/get_wallet_balance/'
        payload = {'user_id': user_id}  # Pass user_id instead of username
        
        response = requests.get(wallet_service_url, params=payload)
        
        if response.status_code == 200:
            wallet_data = response.json()
            context = {
                'user': username,
                'balance': wallet_data['balance'],
                'transactions': wallet_data['transactions']
            }
            return render(request, 'wallet_balance.html', context)
        else:
            return JsonResponse({'error': 'Failed to fetch wallet data'}, status=500)
    else:
        return redirect('user_login')

def deposit_view(request):
    if request.method == 'POST':
        username = request.session['username']
        try:
            user = UserDetail.objects.get(uname=username)
            user_id = user.id  # Assuming that the 'id' field in UserDetail is the user_id
        except UserDetail.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=500)
        amount = Decimal(request.POST.get('amount'))
        
        if amount <= 0:
            messages.error(request, 'Amount must be a positive number.')
            return redirect('deposit')
        
        # Send a request to the wallet service to perform a deposit
        wallet_service_url = 'http://localhost:8004/deposit/'
        payload = {
            'user_id': user_id,
            'amount': str(amount)
        }
        
        response = requests.post(wallet_service_url, data=payload)
        
        if response.status_code == 200:
            messages.success(request, 'Deposit successful.')
        else:
            messages.error(request, 'Deposit failed.')
        
        return redirect('wallet:wallet_balance')
    
    return render(request, 'deposit.html')

def withdraw_view(request):
    if request.method == 'POST':
        username = request.session['username']
        
        # Retrieve the user_id from the UserDetail model
        try:
            user = UserDetail.objects.get(uname=username)
            user_id = user.id  # Assuming that the 'id' field in UserDetail is the user_id
        except UserDetail.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=500)
        amount = Decimal(request.POST.get('amount'))

        if amount <= 0:
            messages.error(request, 'Please enter a valid amount.')
        else:
            # Send a request to the wallet service to perform a withdrawal
            wallet_service_url = 'http://localhost:8004/withdraw/'
            payload = {
                'user_id': user_id,
                'amount': str(amount)
            }
            
            response = requests.post(wallet_service_url, data=payload)
            
            if response.status_code == 200:
                messages.success(request, 'Withdrawal successful.')
            else:
                messages.error(request, 'Withdrawal failed.')
        
        return redirect('wallet:wallet_balance')

    return render(request, 'withdraw.html')

def transfer_view(request):
    if request.method == 'POST':
        username = request.session['username']
        
        # Retrieve the user_id from the UserDetail model
        try:
            user = UserDetail.objects.get(uname=username)
            user_id = user.id  # Assuming that the 'id' field in UserDetail is the user_id
        except UserDetail.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=500)
        amount = Decimal(request.POST.get('amount'))
        recipient = request.POST.get('recipient')
        
        # Check if recipient username is valid (possibly by querying the wallet service)
        # If the recipient is valid, proceed with the transfer request
        
        # Send a request to the wallet service to perform a transfer
        wallet_service_url = 'http://localhost:8004/transfer/'
        payload = {
            'sender_id': user_id,
            'recipient_id': recipient,
            'amount': str(amount)
        }
        
        response = requests.post(wallet_service_url, data=payload)
        
        if response.status_code == 200:
            messages.success(request, 'Transfer successful.')
        else:
            messages.error(request, 'Transfer failed.')
        
        return redirect('wallet:wallet_balance')

    return render(request, 'transfer.html')

def wallet_payment_view(request):
    if request.method == 'POST':
        username = request.session['username']
        try:
            user = UserDetail.objects.get(uname=username)
            user_id = user.id  # Assuming that the 'id' field in UserDetail is the user_id
        except UserDetail.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=500)

        amount = Decimal(request.POST.get('amount'))
        
        # Check if the user has sufficient balance for the payment
        
        # Send a request to the wallet service to initiate a payment
        wallet_service_url = 'http://localhost:8004/payment/'
        payload = {
            'user_id': user_id,
            'amount': str(amount)
        }
        
        response = requests.post(wallet_service_url, data=payload)
        
        if response.status_code == 200:
            messages.success(request, 'Payment successful.')
            return redirect('orderconfirm')  # Redirect to the order confirmation page
        else:
            messages.error(request, 'Payment failed.')
            return redirect('checkout')  # Redirect back to the checkout page

    return render(request, 'wallet_payment.html')
