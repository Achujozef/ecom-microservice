from django.db import models
from decimal import Decimal

# Create your models here.
class Wallet(models.Model):
    user = models.IntegerField(default=0)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    

    def deposit(self, amount,type):
        self.balance += Decimal(str(amount))
        self.save()
        transaction = Transaction(wallet=self, amount=amount,type=type)
        transaction.save()

    def withdraw(self, amount,type):
        if self.balance >= amount:
            self.balance -= Decimal(str(amount))
            self.save()
            transaction = Transaction(wallet=self, amount=-amount,type=type)
            transaction.save()
        else:
            raise Exception("Insufficient balance")

    def transfer(self, amount, recipient_wallet):
        if self.balance >= amount:
            self.balance -= Decimal(str(amount))
            recipient_wallet.balance += Decimal(str(amount))
            self.save()
            recipient_wallet.save()
            transaction = Transaction(wallet=self, amount=-amount)
            transaction.save()
            transaction = Transaction(wallet=recipient_wallet, amount=amount)
            transaction.save()
        else:
            raise Exception("Insufficient balance")
    def get_transaction_history(self):
        return Transaction.objects.filter(wallet=self).order_by('-timestamp')
    
class Transaction(models.Model):
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=200,null=True,default='Transfer')
    def __str__(self):
        return f"Transaction ID: {self.id} | Wallet: {self.wallet} | Amount: {self.amount} | Timestamp: {self.timestamp} | Type:{self.type}"