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

    # def save(self, *args, **kwargs):
    #     self.slug = slugify(self.category_name)
    #     super(Category, self).save(*args, **kwargs)

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
    added_by = models.CharField(max_length=255, default="Ecom")
    product_name = models.CharField(max_length=255)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products",
        blank=True,
        null=True,
    )
    slug = models.SlugField(
        unique=True,
        null=True,
        blank=True,
        help_text=("not required"),
    )
    company = models.CharField(max_length=255, null=True, blank=True, default="Ecom")
    web = models.CharField(max_length=255, null=True, blank=True, default="Ecom.com")
    company_mail = models.CharField(
        max_length=255, null=True, blank=True, default="Ecom@gmail.com"
    )
    price = models.IntegerField()
    product_description = models.TextField()
    color_varient = models.ManyToManyField(ColorVarient, blank=True)
    size_varient = models.ManyToManyField(SizeVarient, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.product_name + str(self.uid)[:7])
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.product_name

    def get_price_by_size(self, size):
        return self.price + SizeVarient.objects.get(size_name=size).price

    def get_price_by_color(self, color):
        return self.price + ColorVarient.objects.get(color_name=color).price


# to filter by price range greather or lesser we can use products.objects.filter(price__gt=1000) i.e for greather or similarly (price__lt=1000) for lesser


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
