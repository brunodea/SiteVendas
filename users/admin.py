from users.models import Costumer, Cart, CartProduct
from django.contrib import admin

class CostumerInline(admin.TabularInline):
    model = Costumer
    extra = 3

class CartProductInline(admin.TabularInline):
    model = CartProduct
    extra = 3

class CartAdmin(admin.ModelAdmin):
    inlines = [CostumerInline, CartProductInline]

admin.site.register(Cart, CartAdmin)

