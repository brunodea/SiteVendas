from django.shortcuts import render_to_response
from django.template import RequestContext
from products.forms import AddProductForm, type_choices, typeChoices
from products.models import Brand, Category, ProductType, Product

def addProductPOSTHandler(post_request):
    
    product_exists = True

    try:
        brand = Brand.objects.get(name=post_request['brand'])
    except Brand.DoesNotExist:
        brand = Brand(name=post_request['brand'])
        brand.save()
        product_exists = False
    
    try:
        category = Category.objects.get(name=post_request['category'])
    except Category.DoesNotExist:
        category = Category(name=post_request['category'])
        category.save()
        product_exists = False
    
    try:
        ptype = ProductType.objects.get(name=post_request['ptype'])
    except ProductType.DoesNotExist:
        ptype = ProductType(name=post_request['ptype'], category=category)
        ptype.save()
        product_exists = False


    try:
        product = Product.objects.get(name=post_request['name'])
        product = []
    except Product.DoesNotExist:
       if not product_exists:
          product = Product(name=post_request['name'], price=post_request['price'], instock=post_request['units'],
                            brand=brand, ptype=ptype)
          product.save()

    return product
           

def addProduct(request, template_name='products/add_product.html'):
   
    user = request.user

    new_product = []
    new_ptype = False

    if request.method == 'POST':
       addform = AddProductForm(request.POST)

       if 'ptype' in request.POST:     
           choice_tuple = type_choices[int(request.POST['ptype']) - 1]
           if choice_tuple[1] == 'Novo':
               new_ptype = True
           elif addform.is_valid():
               new_product = addProductPOSTHandler(request.POST)
       else:
           new_request = request.POST.copy()
           new_request['ptype'] = request.POST['ptype2']
           if new_request['ptype']:
               new_product = addProductPOSTHandler(new_request)

       if new_product:
           addform_choices = addform.fields['ptype'].choices
           addform_choices.append((len(addform_choices), new_product.ptype.name))   
    else:
       addform = AddProductForm()

    context = {'user': user, 'addform': addform, 'object': new_product, 'new_ptype': new_ptype }
    return render_to_response(template_name, context, context_instance = RequestContext(request))

def listProducts(request, template_name='products/list_products.html', objects = []):

    if not objects:
        objects = Product.objects.all()

    context = {'objects': objects }
    return render_to_response(template_name, context, context_instance = RequestContext(request))

def searchProduct(request):
    objects = []

    print request.POST

    if 'searchName' in request.POST:
        objects = Product.objects.filter(name__startswith=request.POST['searchName'])

    return listProducts(request=request, objects=objects)



