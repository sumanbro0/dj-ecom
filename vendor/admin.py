from django.contrib import admin
from .models import Wallet

# Register your models here.
class WalletAdmin(admin.ModelAdmin):
    readonly_fields = [
        "profile",
        "cash",
    ]


admin.site.register(Wallet, WalletAdmin)
