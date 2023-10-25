from django.db import models

# Create your models here.
class ProductVariant(models.Model):
    product = models.IntegerField()
    variant =models.CharField(max_length=50)
    price = models.IntegerField()
    price_after_offer = models.IntegerField(default=0)
    stock = models.PositiveIntegerField(default=1)
    def __str__(self):
        return f'{self.product} - {self.variant} - {self.price}'

    def update_price_with_offer(self, offer_percentage):
        original_price = self.price
        if offer_percentage > 0:
            discounted_price = original_price - (original_price * offer_percentage / 100)
            self.price_after_offer = discounted_price
        else:
            self.price_after_offer = original_price
        self.save()

    def restore_original_prices(self):
        original_price = self.price
        self.price_after_offer = original_price
        self.save()
    def set_price(self, new_price):
        self.price = new_price
        self.update_price_with_offer(self.product.offer_percentage)
        self.save()