from django.shortcuts import render_to_response
from django.template import RequestContext
from products.forms import AddProductForm
import products.forms
from products.models import Brand, Category, ProductType, Product

def addProduct(request, template_name='products/add_product.html'):
    if request.method == 'POST':
        addform = AddProductForm(request.POST)

        if addform.is_valid():
            data = addform.cleaned_data

            product = Product(name=data['name'], price=data['price'], instock=data['units'],
                    ptype=data['ptype'], brand=data['brand'])
            product.save()

            addform = None
    else:
        addform = AddProductForm()

    context = {'user': request.user, 'addform': addform}

    return render_to_response(template_name, context, context_instance = RequestContext(request))


def listProducts(request, template_name='products/list_products.html', objects = []):
    if not objects:
        objects = Product.objects.all()

    context = {'objects': objects }
    return render_to_response(template_name, context, context_instance = RequestContext(request))


def searchProduct(request):
    objects = []
    searchField = 'searchField'

    if searchField in request.GET:
        searchBy = request.GET['searchBy']

        if searchBy == 'name':
            objects = Product.objects.filter(name__startswith=request.GET[searchField])
        elif searchBy == 'type':
            objects = Product.objects.filter(ptype__name__startswith=request.GET[searchField])
        elif searchBy == 'category':
            objects = Product.objects.filter(ptype__category__name__startswith=request.GET[searchField])
        elif searchBy == 'brand':
            objects = Product.objects.filter(brand__name__startswith=request.GET[searchField])

    return listProducts(request=request, objects=objects)

def editCategories(request, template_name='products/edit_categories.html'):
    context = {'user': request.user}

    if request.method == 'POST':
        op = request.POST.get('operation')
        if op == 'brand':
            context['brand_form'] = form = products.forms.BrandEditForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                obj = Brand() if data['brand'] is None else data['brand']
                obj.name = data['new_name']
                obj.save()
        elif op == 'category':
            context['category_form'] = form = products.forms.CategoryEditForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                obj = Category() if data['category'] is None else data['category']
                obj.name = data['new_name']
                obj.save()
        elif op == 'ptype':
            post_data = request.POST

            # gambiarroso
            if 'ptype' in post_data and len(post_data['ptype']) > 1 and post_data['ptype'][0] == '#':
                new_ptype_cat = int(post_data['ptype'][1:])
                post_data = request.POST.copy()
                post_data['ptype'] = ""
            else:
                new_ptype_cat = None

            context['ptype_form'] = form = products.forms.PTypeEditForm(post_data)
            if form.is_valid():
                data = form.cleaned_data
                obj = ProductType(category=Category.objects.get(pk=new_ptype_cat)) if data['ptype'] is None else data['ptype']
                obj.name = data['new_name']
                obj.save()

    if 'brand_form' not in context:
        context['brand_form'] = products.forms.BrandEditForm()
    if 'category_form' not in context:
        context['category_form'] = products.forms.CategoryEditForm()
    if 'ptype_form' not in context:
        context['ptype_form'] = products.forms.PTypeEditForm()

    return render_to_response(template_name, context, context_instance = RequestContext(request))
