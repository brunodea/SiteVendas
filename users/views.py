from django.shortcuts import render_to_response
from django.template import RequestContext
from users.models import Costumer, Cart
from users.forms import SignupForm, UserCreationFormExtended
from products.models import Product

def index(request):
   
    user = request.user
    return render_to_response("basic/base.html", {"user": user }, context_instance = RequestContext(request))


def registerPOSTHandler(post_request, new_user):
    """ Salva um novo medico relacionado a um novo usuario. """    

    cart = Cart()
    cart.save()

    costumer = Costumer(cart=cart, user=new_user)
    costumer.save()

    return costumer

def register(request, template_name='registration/register.html'):
    """ Lida com o cadastro de um usuario. """

    cpf_error_message = []
    new_costumer      = []

    if request.method == 'POST':

       cpf = request.POST['cpf']
       if cpf.isdigit() and not len(cpf) == 11:
           cpf_error_message = "CPF deve ter 11 digitos."

       #inicializa os  formularios com as informacoes obtidas do request.POST.
       signup_form = SignupForm(request.POST)
       regis_form = UserCreationFormExtended(request.POST)

       #caso esteja tudo ok, um novo usuario eh criado.
       if not cpf_error_message and signup_form.is_valid() and regis_form.is_valid():
          new_user = regis_form.save(request.POST)
          new_costumer = registerPOSTHandler(request.POST, new_user)
            
    else:
       signup_form = SignupForm()
       regis_form = UserCreationFormExtended()


    context = {'object': new_costumer, 'signup_form': signup_form,
               'regis_form': regis_form, 'cpf_error_form': cpf_error_message}

    return render_to_response(template_name, context, context_instance = RequestContext(request))

def addProductsToCart(request):

    products = []

    if not request.user.is_authenticated():
        for element in request.POST:
            product = element.split('_')
            if product[0] == 'checkbox':
                request.session['productid'+ '_' + product[1]] = product[1]


    for element in request.session.keys():
        product = element.split('_')
        if product[0] == 'productid':
            products.append(Product.objects.get(id = product[1]))

    return products
    

def userCart(request, template_name='user/user_cart.html'):

    products = addProductsToCart(request)
    context = {'objects': products}

    return render_to_response(template_name, context, context_instance = RequestContext(request))





