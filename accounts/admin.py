from django.contrib import admin
from .models import Cart, CartItems, Orders, Profile
from vendor.models import VerifyImage
from django.utils.html import format_html

# Register your models here.


class cartItemsAdmin(admin.StackedInline):
    model = CartItems


class cartAdmin(admin.ModelAdmin):
    list_display = ("user", "token", "is_paid", "is_orderd")
    inlines = [cartItemsAdmin]


admin.site.register(Cart, cartAdmin)
# admin.site.register(CartItems, cartItemsAdmin)


class VerifyImageAdmin(admin.StackedInline):
    model = VerifyImage


class profileAdmin(admin.ModelAdmin):
    def myphoto(self, object):
        try:
            return format_html(
                '<img src="{}" width="40px" />'.format(object.profile_image.url)
            )
        except Exception as e:
            print(e)

    inlines = [VerifyImageAdmin]
    list_display = ("myphoto", "user", "is_email_verified", "is_vendor")
    list_display_links = ("myphoto", "user")
    search_fields = ("user__username",)
    # list_filter = ("camera_type", "category")
    list_editable = ("is_email_verified", "is_vendor")


class orderAdmin(admin.ModelAdmin):

    list_display = ("name", "cart", "is_delevered", "is_orderd", "is_shipped")
    search_fields = ("name",)
    list_editable = ("is_delevered", "is_orderd", "is_shipped")


admin.site.register(Profile, profileAdmin)
admin.site.register(Orders, orderAdmin)
