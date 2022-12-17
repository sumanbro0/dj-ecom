from django.shortcuts import render

from .models import Category, ColorVarient, Product, ProductImage, SizeVarient
from django.contrib import messages
from accounts.models import Profile

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


def add_product(request):
    cat = Category.objects.all()
    cate = None
    user = Profile.objects.get(user=request.user)
    if request.method == "POST":

        product_name = request.POST.get("product_name")
        product_category = request.POST.get("product_category")
        print(product_category)
        if product_category != "All":
            cate = Category.objects.get(category_name=product_category)
        product_description = request.POST.get("product_description")
        price = request.POST.get("product_base_price")
        company = request.POST.get("company")
        website = request.POST.get("website")
        company_mail = request.POST.get("company_mail")
        s = request.POST.get("size_count")
        c = request.POST.get("color_count")
        su = []
        cu = []
        if s:
            for i in range(int(s)):
                size_name = request.POST.get(f"size_name{i}")
                size_price = request.POST.get(f"size_price{i}")
                sv = SizeVarient.objects.get_or_create(
                    size_name=size_name, price=size_price
                )
                su.append(sv[0].uid)
        if c:
            for i in range(int(c)):
                color_name = request.POST.get(f"color_name{i}")
                color_price = request.POST.get(f"color_price{i}")
                cv = ColorVarient.objects.get_or_create(
                    color_name=color_name, price=color_price
                )
                cu.append(cv[0].uid)
        try:
            product = Product(
                added_by=request.user.username,
                product_name=product_name,
                category=cate,
                company=company,
                web=website,
                slug=None,
                company_mail=company_mail,
                price=price,
                product_description=product_description,
            )
            product.save()
            product.color_varient.add(*cu)
            product.size_varient.add(*su)
            product.save()
        except Exception as e:
            print(e)
            messages.warning(request, "product already exists")
        imgs = request.FILES.getlist(f"images")
        for imgx in imgs:
            img = ProductImage(product=product, image=imgx)
            img.save()
        messages.success(request, "items added")
    return render(
        request, "products/addProduct.html", context={"cat": cat, "users": user}
    )
