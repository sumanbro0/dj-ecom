from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from accounts.models import Orders, Profile
from accounts.views import logout_view
from ecom import settings
from products.models import Category, Product
from django.contrib import messages
from django.contrib.auth.models import User
from base import emails

# Create your views here.
def index(request):
    category = Category.objects.all()
    products = Product.objects.all()
    context = {"category": category, "products": products}
    try:
        profile = Profile.objects.get(user=request.user)
        context["profile"] = profile
    except Exception as e:
        print(e)
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


def change(request):
    if request.method == "POST":
        user = request.POST.get("email")
        try:
            if User.objects.get(username=user):
                email = user
                uid = User.objects.get(username=user).id
                emails.send_change_password_email(email, uid)
                messages.success(
                    request,
                    "An email has been sent to you please check your mail to proceed",
                )
        except Exception as e:
            print(e)
            messages.warning(request, "user doesnot exists")
    return render(request, "home/change.html")


def change_pwd(request, uid):
    try:
        id = uid
        user = User.objects.get(id=id)
        if request.method == "POST":
            password1 = request.POST.get("new_password")
            password2 = request.POST.get("confirm_password")
            if password1 == password2:
                user.set_password(password2)
                user.save()
                logout_view(request)
                messages.success(request, "password changed")
                return redirect("login_page")
            else:
                messages.warning(request, "passwords dont match")
                return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
    except Exception as e:
        print(e)
        messages.warning(request, "invalid credentials! try again")
        return render(request, "home/change.html")
    return render(request, "home/new_pwd.html")


def change_name(request, id):
    try:
        user = User.objects.get(id=id)
        if request.method == "POST":
            user.first_name = request.POST.get("first_name")
            user.last_name = request.POST.get("last_name")
            user.save()
            messages.success(request, "your name have been changed")
    except Exception as e:
        print(e)
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
