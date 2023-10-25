from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST,require_GET
from decimal import Decimal
from django.core.exceptions import ObjectDoesNotExist
from .models import Wallet, Transaction


@require_POST
def deposit_view(request):
    try:
        user_id = request.POST['user_id']
        amount = Decimal(request.POST['amount'])
        wallet = Wallet.objects.get(user=user_id)
        wallet.deposit(amount, "Deposit")
        return JsonResponse({'message': 'Deposit successful'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@require_POST
def withdraw_view(request):
    try:
        user_id = request.POST['user_id']
        amount = Decimal(request.POST['amount'])
        wallet = Wallet.objects.get(user=user_id)
        wallet.withdraw(amount, "Withdrawed")
        return JsonResponse({'message': 'Withdrawal successful'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@require_POST
def transfer_view(request):
    try:
        sender_id = request.POST['sender_id']
        recipient_id = request.POST['recipient_id']
        amount = Decimal(request.POST['amount'])

        sender_wallet = Wallet.objects.get(user=sender_id)
        recipient_wallet = Wallet.objects.get(user=recipient_id)

        sender_wallet.transfer(amount, recipient_wallet)
        return JsonResponse({'message': 'Transfer successful'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@require_POST
def payment_view(request):
    try:
        user_id = request.POST['user_id']
        amount = Decimal(request.POST['amount'])
        wallet = Wallet.objects.get(user=user_id)

        if wallet.balance >= amount:
            wallet.withdraw(amount, 'Paid For Order')
            # Handle additional logic for order processing if needed
            return JsonResponse({'message': 'Payment successful'})
        else:
            return JsonResponse({'error': 'Insufficient balance'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
    
@require_GET
def get_wallet_balance(request):
    if request.method == 'GET':
        try:
            user_id = request.GET.get('user_id')
            wallet = Wallet.objects.get(user=user_id)
            balance = wallet.balance

            # Get the transaction history for the wallet
            transactions = Transaction.objects.filter(wallet=wallet).order_by('-timestamp')
            transaction_data = []
            for transaction in transactions:
                transaction_data.append({
                    'amount': str(transaction.amount),
                    'timestamp': transaction.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                    'type': transaction.type,
                })

            response_data = {
                'balance': str(balance),
                'transactions': transaction_data,
            }

            return JsonResponse(response_data)
        except Wallet.DoesNotExist:
            return JsonResponse({'error': 'Wallet not found for the user'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)