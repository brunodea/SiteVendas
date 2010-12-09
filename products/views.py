from django.shortcuts import render_to_response
from django.template import RequestContext
from products.forms import AddProductForm
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
