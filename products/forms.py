from django import forms
from products.models import ProductType

def typeChoices():
    choices = []
    i = 1
    for pt in ProductType.objects.all():
        choices.append((i, pt.name))
        i += 1
    choices.append((i, 'Novo'))
    print choices
    return choices

type_choices = typeChoices()

class AddProductForm(forms.Form):
    name = forms.CharField(max_length=30, required=True, initial='', label='Nome')
    price = forms.FloatField(min_value=0.0, required=True, initial=0.0, label='Preco')
    units = forms.IntegerField(min_value=0, required=True, initial=0, label='Quantidade')
    brand = forms.CharField(max_length=100, required=True, initial='', label='Marca')
    category = forms.CharField(max_length=100, required=True, initial='', label='Categoria')
    ptype = forms.ChoiceField(choices=type_choices, required=True, initial='', label='Tipo')
    ptype2 = forms.CharField(max_length=100, required=False, initial='', label='Categoria')
#    image = forms.ImageField(required=True, label='Imagem')


    def __unicode__(self):
        return 'Add Product Form'

