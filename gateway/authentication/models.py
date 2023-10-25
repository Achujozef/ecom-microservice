from django.db import models
from decimal import Decimal
# Create your models here.
class MyAdmin(models.Model):
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)

class UserDetail(models.Model):
    uname=models.CharField(unique=True, max_length=50)
    uemail=models.CharField(max_length=50)
    phone=models.CharField(max_length=50, null=True)
    upassword=models.CharField(max_length=50)
    uactive=models.BooleanField(default=True)
    uimage = models.ImageField(upload_to='imagestore/', null=True, blank=True)
    uotp=models.IntegerField(null=True)
    def __str__(self): 
        return self.uname 

STATE_CHOICES = (
    ('KARNATAKA', 'KARNATAKA'),
    ('KERALA', 'KERALA'),
    ('TAMIL NADU', 'TAMIL NADU'),
    ('GOA', 'GOA'),
    ('GUJARAT', 'GUJARAT')
)

class Address(models.Model):
    user = models.ForeignKey(UserDetail, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=12)
    housename = models.CharField(max_length=50)
    locality = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    zipcode = models.IntegerField()
    state = models.CharField(choices=STATE_CHOICES, max_length=50, default='KERALA')
    selected = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)