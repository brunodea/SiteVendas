from products.models import Brand, Category, ProductType, Product
from django.contrib import admin


class ProductInline(admin.TabularInline):
    model = Product
    extra = 3

class ProductTypeInline(admin.TabularInline):
    model = ProductType
    extra = 3

class CategoryInline(admin.TabularInline):
    model = Category
    extra = 3

class BrandInline(admin.TabularInline):
    model = Brand
    extra = 3

class BrandAdmin(admin.ModelAdmin):
    inlines = [ProductInline]

class ProductTypeAdmin(admin.ModelAdmin):
    inlines = [ProductInline]

class CategoryAdmin(admin.ModelAdmin):
    inlines = [ProductTypeInline]

class ProductAdmin(admin.ModelAdmin): pass

admin.site.register(Brand, BrandAdmin)
admin.site.register(ProductType, ProductTypeAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)

