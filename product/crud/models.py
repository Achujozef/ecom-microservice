from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=200, default='')
    stock = models.PositiveIntegerField(default=1)
    category = models.IntegerField(default=0)
    normalprice = models.IntegerField(default=0)
    listed = models.BooleanField(default=True)
    offer_percentage = models.IntegerField(default=0,null=True)

    def __str__(self):
        return self.name

class Image(models.Model):
    image = models.ImageField(upload_to='products/')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True, related_name='images', default=None)
    
    
    def __str__(self):
        return self.image.name
