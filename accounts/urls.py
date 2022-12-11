from . import views
from django.urls import path


urlpatterns = [
    path("login/", views.login_page, name="login_page"),
    path("register/", views.register_page, name="register_page"),
    path("activate/<email_token>/", views.activate_email, name="activate_email"),
    path("logout/", views.logout_view, name="logout"),
    path("cart/", views.cart, name="cart"),
    path("add-to-cart/<uid>/", views.add_to_cart, name="add_to_cart"),
    path("remove-cart/<uid>/", views.remove_cart, name="remove_cart"),
    path("checkout/", views.checkout, name="checkout"),
    path("remove-coupon/<uid>/", views.remove_coupon, name="remove_coupon"),
    path("delete-order/<uid>/", views.delete_orders, name="delete_orders"),
    path("verify-payment", views.verify_payment, name="verify_payment"),
    path("make-pur/", views.make_pur, name="make_pur"),
    path("profile/", views.profile, name="profile"),
    path("save-image/", views.save_image, name="save_image"),
]
