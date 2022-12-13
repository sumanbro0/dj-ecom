from django.shortcuts import render

from .models import Product

# Create your views here.
def get_product(request, slug):
    try:
        product = Product.objects.get(slug=slug)
        context = {
            "product": product,
            "updated_price": product.price,
            "qty": 1,
        }

    except Exception as e:
        print(e)
    return render(request, "products/product.html", context)
