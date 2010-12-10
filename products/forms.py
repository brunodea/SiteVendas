from django import forms
from products.models import Brand, Category, ProductType

def get_ptype_choices(empty_string=None):
    choices = []

    for cat in Category.objects.order_by('name'):
        ptypes = [(ptype.pk, ptype.name) for ptype in
                ProductType.objects.filter(category=cat.pk).order_by('name')]
        if empty_string is not None:
            ptypes.insert(0, ('#'+str(cat.pk), empty_string))
        choices.append((cat.name, ptypes))

    return choices

class CustomModelChoiceField(forms.ModelChoiceField):
    def __init__(self, choice_provider, *args, **kwargs):
        self.choice_provider = choice_provider
        super(CustomModelChoiceField, self).__init__(*args, **kwargs)

    def _make_generator(self, f):
        for i in f():
            yield i

    def _get_choices(self):
        return self._make_generator(self.choice_provider)

    choices = property(_get_choices, forms.ChoiceField._set_choices)

class AddProductForm(forms.Form):
    name = forms.CharField(max_length=30, required=True, initial='', label='Nome')
    price = forms.DecimalField(min_value=0.0, required=True, initial=0.0, label='Preco',
            max_digits=7, decimal_places=2)
    units = forms.IntegerField(min_value=0, required=True, initial=0, label='Quantidade')
    brand = forms.ModelChoiceField(queryset=Brand.objects.order_by('name'), empty_label=None,
            required=True, label='Marca')
    ptype = CustomModelChoiceField(queryset=ProductType.objects, choice_provider=get_ptype_choices,
            required=True, label='Categoria e Tipo')

    def __unicode__(self):
        return 'Add Product Form'


class BrandEditForm(forms.Form):
    brand = forms.ModelChoiceField(queryset=Brand.objects.order_by('name'), empty_label='<Nova>',
            required=False, label='Marca')
    new_name = forms.CharField(max_length=100, required=True, initial='', label='Novo nome')


class CategoryEditForm(forms.Form):
    category = forms.ModelChoiceField(queryset=Category.objects.order_by('name'), empty_label='<Nova>',
            required=False, label='Categoria')
    new_name = forms.CharField(max_length=100, required=True, initial='', label='Novo nome')


class PTypeEditForm(forms.Form):
    ptype = CustomModelChoiceField(queryset=ProductType.objects, required=False, label='Categoria e Tipo',
            choice_provider=(lambda: get_ptype_choices(empty_string='<Nova>')))
    new_name = forms.CharField(max_length=100, required=True, initial='', label='Novo nome')
