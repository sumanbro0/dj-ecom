from django.shortcuts import render

from .models import Product

# Create your views here.
def get_product(request, slug):
    try:
        product = Product.objects.get(slug=slug)
        context = {"product": product, "updated_price": 0}
        context["updated_size_price"] = 0
        context["updated_color_price"] = 0
        context["qty"] = 1
        if request.GET.get("size"):
            size = request.GET.get("size")
            price = product.get_price_by_size(size) - product.price
            context["slected_size"] = size
            context["updated_size_price"] = price

        if request.GET.get("color"):
            color = request.GET.get("color")
            price = product.get_price_by_color(color) - product.price
            context["slected_color"] = color
            context["updated_color_price"] = int(price)
        if request.GET.get("qty"):
            qty = request.GET.get("qty")
            context["qty"] = int(qty)
        context["updated_price"] = (
            context["updated_color_price"] * context["qty"]
            + context["updated_size_price"] * context["qty"]
            + product.price * context["qty"]
        )

    except Exception as e:
        print(e)
    return render(request, "products/product.html", context)
