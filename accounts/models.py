from django.db import models
from base.models import BaseModel
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid
from base.emails import send_account_activation_email
from products.models import ColorVarient, Coupon, Product, SizeVarient

# Create your models here.
class Profile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    is_email_verified = models.BooleanField(default=False)
    email_token = models.CharField(max_length=255, null=True, blank=True)
    profile_image = models.ImageField(upload_to="media/profile/%Y")

    def get_cart_count(self):
        return CartItems.objects.filter(
            cart__is_orderd=False, cart__user=self.user
        ).count()

    def __str__(self) -> str:
        return self.user.first_name


class Cart(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="carts")
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True)
    token = models.CharField(max_length=255, null=True, blank=True)
    is_paid = models.BooleanField(default=False)
    is_orderd = models.BooleanField(default=False)

    def get_cart_total(self):
        cart_items = self.cart_items.all()
        price = []
        for cart_item in cart_items:
            price.append(cart_item.get_product_price())
        if self.coupon:
            if self.coupon.minimum_amount < sum(price):
                return sum(price) - self.coupon.discount_price
        return sum(price)

    def __str__(self) -> str:
        return self.user.first_name


class CartItems(BaseModel):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cart_items")
    product = models.ForeignKey(
        Product, on_delete=models.SET_NULL, null=True, blank=True
    )
    quantity = models.IntegerField(default=0)
    color_varient = models.ForeignKey(
        ColorVarient, on_delete=models.SET_NULL, null=True, blank=True
    )
    size_varient = models.ForeignKey(
        SizeVarient, on_delete=models.SET_NULL, null=True, blank=True
    )

    def get_product_price(self):
        price = [self.product.price]
        if self.color_varient:
            color_var_price = self.color_varient.price
            price.append(color_var_price)
        if self.size_varient:
            size_var_price = self.size_varient.price
            price.append(size_var_price)
        return sum(price) * self.quantity

    def __str__(self) -> str:
        return f"{self.product.product_name}-{self.color_varient}-{self.size_varient}"


@receiver(post_save, sender=User)
def send_email_token(sender, instance, created, **kwargs):
    try:
        if created:
            email_token = str(uuid.uuid4())
            Profile.objects.create(user=instance, email_token=email_token)
            email = instance.email
            send_account_activation_email(email, email_token)

    except Exception as e:
        print(e)


class Orders(BaseModel):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="carts")
    is_shipped = models.BooleanField(default=False)
    is_orderd = models.BooleanField(default=False)
    is_delevered = models.BooleanField(default=False)
    amount = models.IntegerField(default=0, null=True, blank=True)
    name = models.CharField(max_length=90, null=True, blank=True)
    email = models.CharField(max_length=90, null=True, blank=True)
    address1 = models.CharField(max_length=90, null=True, blank=True)
    address2 = models.CharField(max_length=90, null=True, blank=True)
    city = models.CharField(max_length=90, null=True, blank=True)
    state = models.CharField(max_length=90, null=True, blank=True)
    zip = models.CharField(max_length=10, null=True, blank=True)
    phone = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self) -> str:
        return self.name
