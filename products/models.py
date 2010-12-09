from django.db import models

class Brand(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name


class ProductType(models.Model):
    category = models.ForeignKey(Category)
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    instock = models.IntegerField()

    ptype = models.ForeignKey(ProductType)
    brand = models.ForeignKey(Brand)

    def __unicode__(self):
        return self.name
