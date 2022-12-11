from django.shortcuts import render
from accounts.models import Orders
from products.models import Category, Product
from django.contrib import messages

# Create your views here.
def index(request):
    category = Category.objects.all()
    products = Product.objects.all()
    context = {
        "category": category,
        "products": products,
    }
    if request.GET:
        if request.GET.get("category") != "all":
            cat = request.GET.get("category")
            c = Category.objects.get(slug=cat)
            products = Product.objects.filter(category=c)
            context["products"] = products
            context["slected"] = c
    return render(request, "home/index.html", context)


def track(request):
    if request.method == "POST":
        id = request.POST.get("order_id")
        try:
            order = Orders.objects.get(uid=id)
            if order.is_orderd and order.is_shipped and order.is_delevered:
                messages.success(request, "Your order have already been delevered")
            elif order.is_orderd and order.is_shipped:
                messages.success(
                    request, "Your order have been shipped and will be delevered soon"
                )
            elif order.is_orderd:
                messages.success(
                    request, "Your order have been placed and will be delevered soon"
                )
        except Exception as e:
            print(e)
            messages.warning(request, "order doesnot exists")

    return render(request, "products/track.html")


def category(request):
    pass


def search(request):
    products = Product.objects.order_by("-created_at")
    keyword = ""
    if "keyword" in request.GET:
        keyword = request.GET["keyword"]
        if keyword != None:
            product = products.filter(product_name__icontains=keyword)
            if not product:
                product = products.filter(product_description__icontains=keyword)
        if not product:
            messages.warning(request, f"product:-{keyword} not found")
    return render(
        request,
        "home/search.html",
        {"products": product, "keyword": keyword},
    )
