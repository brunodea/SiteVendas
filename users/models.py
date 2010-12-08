from django.db import models
from django.contrib.auth.models import User
from products.models import Product

class Cart(models.Model):
    products = models.ManyToManyField(Product, through='CartProduct')

    def __unicode__(self):
        return 'Cart'


class Costumer(models.Model):
    user = models.ForeignKey(User, unique=True)
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
