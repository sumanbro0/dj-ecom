import json
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from products.models import ColorVarient, Coupon
import requests
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import Orders, Profile
from accounts.models import Cart, CartItems
from .models import Product, SizeVarient

# Create your views here.
def login_page(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user_obj = User.objects.filter(username=email)

        if not user_obj.exists():
            messages.warning(request, "Account not found.")
            return HttpResponseRedirect(request.path_info)

        if not user_obj[0].profile.is_email_verified:
            messages.warning(request, "Your account is not verified.")
            return HttpResponseRedirect(request.path_info)

        user_obj = authenticate(username=email, password=password)
        if user_obj:
            login(request, user_obj)
            return redirect("/")

        messages.warning(request, "Invalid credentials")
        return HttpResponseRedirect(request.path_info)

    return render(request, "accounts/login.html")


def register_page(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        user_obj = User.objects.filter(username=email)
        if user_obj.exists():
            messages.warning(request, "Email already taken")
            return HttpResponseRedirect(request.path_info)
        user = User.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            username=email,
        )
        user.set_password(password)
        user.save()
        messages.success(
            request,
            "email has been sent to your email account please verify your account to proceed",
        )
        return HttpResponseRedirect(request.path_info)
    return render(request, "accounts/register.html")


def activate_email(request, email_token):
    try:
        user = Profile.objects.get(email_token=email_token)
        user.is_email_verified = True
        user.save()
        return redirect("/")
    except Exception as e:
        return HttpResponse("invalid token")


def logout_view(request):
    logout(request)
    return redirect("/")


def add_to_cart(request, uid):
    size = request.GET.get("size")
    color = request.GET.get("color")
    qty = request.GET.get("qty")
    product = Product.objects.get(uid=uid)
    try:
        user = request.user
        cart, _ = Cart.objects.get_or_create(user=user, is_orderd=False)
        try:
            if product.color_varient.all().first() == None:
                item = CartItems.objects.get_or_create(
                    cart=cart,
                    product=product,
                    size_varient=SizeVarient.objects.get(size_name=size),
                )
                item[0].quantity += int(qty)
                item[0].save()
            elif product.size_varient.all().first() == None:
                item = CartItems.objects.get_or_create(
                    cart=cart,
                    product=product,
                    color_varient=ColorVarient.objects.get(color_name=color),
                )
                item[0].quantity += int(qty)
                item[0].save()
            elif (
                product.size_varient.all().first() == None
                and product.color_varient.all().first() == None
            ):
                item = CartItems.objects.get_or_create(
                    cart=cart,
                    product=product,
                )
                item[0].quantity += int(qty)
                item[0].save()
            else:
                item = CartItems.objects.get_or_create(
                    cart=cart,
                    product=product,
                    size_varient=SizeVarient.objects.get(size_name=size),
                    color_varient=ColorVarient.objects.get(color_name=color),
                )
                item[0].quantity += int(qty)
                item[0].save()

            messages.success(request, f"Item {product.product_name} added to cart")

        except Exception as e:
            if product.size_varient.all().first() != None and not size:
                messages.warning(request, f"please choose size")
            elif product.color_varient.all().first() != None and not color:
                messages.warning(request, f"please choose color")
            else:
                messages.warning(request, f"please choose size and color")
    except Exception as e:
        messages.warning(request, "Please login to add to cart")
        return redirect("login_page")
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


def remove_cart(request, uid):
    try:
        cart_item = CartItems.objects.get(uid=uid)
        cart_item.delete()
        messages.warning(request, f"Item removed from cart")
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
    except Exception as e:
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


def cart(request):
    cart = None
    try:
        cart = Cart.objects.get(is_orderd=False, user=request.user)
        if request.GET.get("pid"):
            product = Product.objects.get(uid=request.GET.get("pid"))
            if request.GET.get("color") and request.GET.get("size"):
                cart_item = CartItems.objects.get(
                    product=product,
                    cart=cart,
                    color_varient=ColorVarient.objects.get(
                        color_name=request.GET.get("color")
                    ),
                    size_varient=SizeVarient.objects.get(
                        size_name=request.GET.get("size")
                    ),
                )
                cart_item.quantity = request.GET.get("qty")
                cart_item.save()
            elif request.GET.get("color") and not request.GET.get("size"):
                cart_item = CartItems.objects.get(
                    product=product,
                    cart=cart,
                    color_varient=ColorVarient.objects.get(
                        color_name=request.GET.get("color")
                    ),
                )
                cart_item.quantity = request.GET.get("qty")
                cart_item.save()
            elif not request.GET.get("color") and request.GET.get("size"):
                cart_item = CartItems.objects.get(
                    product=product,
                    cart=cart,
                    size_varient=SizeVarient.objects.get(
                        size_name=request.GET.get("size")
                    ),
                )
                cart_item.quantity = request.GET.get("qty")
                cart_item.save()
            else:
                cart_item = CartItems.objects.get(
                    product=product,
                    cart=cart,
                )
                cart_item.quantity = request.GET.get("qty")
                cart_item.save()

    except Exception as e:
        print(e)
    if request.method == "POST":
        coupon = request.POST.get("coupon")
        coupon_obj = Coupon.objects.filter(coupon_code__icontains=coupon)
        if not coupon_obj.exists():
            messages.warning(request, "Invalid coupon.")
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
        if cart.coupon:
            messages.warning(request, "coupon already applied")
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
        if cart.get_cart_total() < coupon_obj[0].minimum_amount:
            messages.warning(
                request,
                f"minimum amount of {coupon_obj[0].minimum_amount} required to apply coupon",
            )
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
        if coupon_obj[0].is_expired:
            messages.warning(
                request,
                f"coupon has been expired",
            )
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

        cart.coupon = coupon_obj[0]
        cart.save()
        messages.success(request, "coupon applied")
    if cart:
        return render(request, "carts/cart.html", context={"cart": cart})
    else:
        return render(request, "carts/cart.html")


def remove_coupon(request, uid):
    cart = Cart.objects.get(uid=uid)
    cart.coupon = None
    cart.save()
    messages.success(
        request,
        f"coupon has been removed",
    )
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


def verify_payment(request):
    if request.body:
        data = json.loads(request.body.decode("utf-8"))
        token = data["token"]
        amount = data["amount"]
        url = "https://khalti.com/api/v2/payment/verify/"
        payload = {"token": token, "amount": amount}
        headers = {
            "Authorization": "Key test_secret_key_f68b962353fa41f9977cd4a0ba56ecbb"
        }

        response = requests.post(url, payload, headers=headers)
        response_data = json.loads(response.text)
        uid = response_data["product_identity"]
        cart = Cart.objects.get(uid=uid)
        cart.is_paid = True
        cart.token = token
        cart.save()
        return JsonResponse(f"payment done:{response_data['user']}", safe=False)

    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


@login_required()
def checkout(request):
    if request.method == "POST":
        data = request.POST.get("id")
        cart = Cart.objects.get(uid=data)
        cart.is_orderd = True
        amount = cart.get_cart_total()
        name = request.POST.get("name")
        email = request.POST.get("email")
        address1 = request.POST.get("address1")
        address2 = request.POST.get("address2")
        city = request.POST.get("city")
        state = request.POST.get("state")
        zip = request.POST.get("zip")
        phone = request.POST.get("phone")
        order = Orders(
            cart=cart,
            amount=amount,
            is_orderd=True,
            name=name,
            email=email,
            address1=address1,
            address2=address2,
            city=city,
            state=state,
            zip=zip,
            phone=phone,
        )
        order.save()
        cart.save()
        return render(
            request, "carts/payment.html", context={"cart": cart, "order_id": order.uid}
        )
    return render(
        request,
        "carts/checkout.html",
    )


def make_pur(request):
    return render(request, "carts/payment.html")


# @login_required()
def profile(request):
    try:
        user = request.user
        profile = Profile.objects.get(user=user)
        cart = Cart.objects.filter(user=user, is_orderd=True)
        orders = []
        for c in cart:
            order = Orders.objects.filter(cart=c)
            orders.append(order)

        return render(
            request,
            "accounts/profile.html",
            context={"carts": cart, "orders": orders, "profile": profile},
        )
    except Exception as e:
        messages.warning(request, "you are not logged in")
        return redirect("login_page")


def delete_orders(request, uid):
    cart = Cart.objects.get(uid=uid)
    order = Orders.objects.get(cart__uid=cart.uid)
    order.delete()
    cart.delete()
    messages.success(request, "Your order have been removed")
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


def save_image(request):
    if request.method == "POST":
        img = request.FILES["img"]
        profile = Profile.objects.get(user=request.user)
        profile.profile_image = img
        profile.save()
        messages.success(request, "successuflly added image")
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
