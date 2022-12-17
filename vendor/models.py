from django.db import models
from accounts.models import Cart, CartItems, Orders, Profile

from base.models import BaseModel
from products.models import Product

# Create your models here.
class VerifyImage(BaseModel):
    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="product_verify_images"
    )
    front = models.ImageField(upload_to="media/verify_vendor", blank=True, null=True)
    back = models.ImageField(upload_to="media/verify_vendor", blank=True, null=True)


class Wallet(BaseModel):
    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="vendor_wallet"
    )
    cash = models.CharField(max_length=4)

    def get_wallet_price(self, request):
        products = Product.objects.filter(added_by=self.profile.user)
        carts = Cart.objects.filter(is_paid=True, is_orderd=True)
        cart_items = []
        for cart in carts:
            cart_item = CartItems.objects.filter(cart=cart)
            cart_items.append(cart_item)
        prices = []

        for product in products:
            for items in cart_items:
                for item in items:
                    if product.uid == item.product.uid:
                        price = int(item.product.price)
                        if item.size_varient:
                            price += int(item.size_varient.price)

                        if item.color_varient:
                            price += int(item.color_varient.price)
                        price = (price - ((price / 100) * 5)) * int(item.quantity)
                        prices.append(price)
        self.cash = sum(prices)
        self.save()
        return self.cash
