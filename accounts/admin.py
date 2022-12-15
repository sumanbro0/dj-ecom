from django.contrib import admin
from .models import Cart, CartItems, Orders, Profile
from django.utils.html import format_html

# Register your models here.
class cartAdmin(admin.ModelAdmin):
    list_display = ("user", "token", "is_paid", "is_orderd")


class cartItemsAdmin(admin.ModelAdmin):
    list_display = ("cart", "product", "quantity")


admin.site.register(Cart, cartAdmin)
admin.site.register(CartItems, cartItemsAdmin)


class profileAdmin(admin.ModelAdmin):
    def myphoto(self, object):
        try:
            return format_html(
                '<img src="{}" width="40px" />'.format(object.profile_image.url)
            )
        except Exception as e:
            print(e)

    list_display = ("myphoto", "user", "is_email_verified")
    # list_display_links = ("name", "id")
    search_fields = ("user__username",)
    # list_filter = ("camera_type", "category")
    list_editable = ("is_email_verified",)


class orderAdmin(admin.ModelAdmin):

    list_display = ("name", "cart", "is_delevered", "is_orderd", "is_shipped")
    search_fields = ("name",)
    list_editable = ("is_delevered", "is_orderd", "is_shipped")


admin.site.register(Profile, profileAdmin)
admin.site.register(Orders, orderAdmin)
