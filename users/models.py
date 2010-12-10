from django.db import models
from django.contrib.auth.models import User
from products.models import Product

class Cart(models.Model):
    products = models.ManyToManyField(Product, through='CartProduct')

    def getNumProduct(self, product):
        try:
            return CartProduct.objects.get(cart=self, product=product).num_prods
        except CartProduct.DoesNotExist:
            return 0

    def setNumProduct(self, product, num):
        try:
            cp = CartProduct.objects.get(cart=self, product=product)
            cp.num_prods = num
        except CartProduct.DoesNotExist:
            cp = CartProduct(cart=self, product=product, num_prods=num)
        if cp.num_prods < 0:
            cp.num_prods = 0
        cp.save()

    def addNumProduct(self, product, num):
        try:
            cp = CartProduct.objects.get(cart=self, product=product)
            cp.num_prods += num
        except CartProduct.DoesNotExist:
            cp = CartProduct(cart=self, product=product, num_prods=num)
        if cp.num_prods < 0:
            cp.num_prods = 0
        cp.save()

    def __unicode__(self):
        return 'Cart'


class Costumer(models.Model):
    user = models.OneToOneField(User)
    cart = models.OneToOneField(Cart)

    def __unicode__(self):
        return self.user.username


class CartProduct(models.Model):
    cart = models.ForeignKey(Cart)
    product = models.ForeignKey(Product)

    #numero de itens de tal produto.
    num_prods = models.IntegerField()

    class Meta:
        unique_together = (("cart", "product"),)

    def __unicode__(self):
        return 'Cart Product'
