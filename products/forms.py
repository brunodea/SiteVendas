from django import forms
from products.models import Brand, Category, ProductType

def get_ptype_choices():
    choices = []
    for cat in Category.objects.order_by('name'):
        ptypes = [(ptype.pk, ptype.name) for ptype in
                ProductType.objects.filter(category=cat.pk).order_by('name')]
        choices.append((cat.name, ptypes))

    return choices

class AddProductForm(forms.Form):
    name = forms.CharField(max_length=30, required=True, initial='', label='Nome')
    price = forms.DecimalField(min_value=0.0, required=True, initial=0.0, label='Preco',
            max_digits=7, decimal_places=2)
    units = forms.IntegerField(min_value=0, required=True, initial=0, label='Quantidade')
    brand = forms.ModelChoiceField(queryset=Brand.objects.order_by('name'), required=True, label='Marca')
    ptype = forms.ModelChoiceField(queryset=ProductType.objects, required=True, label='Categoria e Tipo')
    ptype.choices = get_ptype_choices()

    def __init__(self, *args, **kwargs):
        super(AddProductForm, self).__init__(*args, **kwargs)
        # sort-of-hack: needs update on every instanciation
        self.fields['ptype'].choices = get_ptype_choices()

    def __unicode__(self):
        return 'Add Product Form'
