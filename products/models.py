from django.db import models
from base.models import BaseModel
from django.utils.text import slugify

# Create your models here.
class Category(BaseModel):
    category_name = models.CharField(max_length=255)
    slug = models.SlugField(
        unique=True,
        null=True,
        blank=True,
        help_text=("not required"),
    )
    category_image = models.ImageField(upload_to="media/category")

    def save(self, *args, **kwargs):
        self.slug = slugify(self.category_name)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.category_name


class ColorVarient(BaseModel):
    color_name = models.CharField(max_length=255)
    price = models.IntegerField(default=0)

    def __str__(self):
        return self.color_name


class SizeVarient(BaseModel):
    size_name = models.CharField(max_length=255)
    price = models.IntegerField(default=0)

    def __str__(self):
        return self.size_name


class Product(BaseModel):
    product_name = models.CharField(max_length=255)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="products"
    )
    slug = models.SlugField(
        unique=True,
        null=True,
        blank=True,
        help_text=("not required"),
    )
    price = models.IntegerField()
    product_description = models.TextField()
    color_varient = models.ManyToManyField(ColorVarient, blank=True)
    size_varient = models.ManyToManyField(SizeVarient, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.product_name)
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.product_name

    def get_price_by_size(self, size):
        return self.price + SizeVarient.objects.get(size_name=size).price

    def get_price_by_color(self, color):
        return self.price + ColorVarient.objects.get(color_name=color).price


class ProductImage(BaseModel):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="product_images"
    )
    image = models.ImageField(upload_to="media/products")


class Coupon(BaseModel):
    coupon_code = models.CharField(max_length=25)
    is_expired = models.BooleanField(default=False)
    discount_price = models.IntegerField(default=100)
    minimum_amount = models.IntegerField(default=500)

    def __str__(self):
        return str(self.uid)
