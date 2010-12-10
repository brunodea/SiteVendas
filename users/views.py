from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from users.models import Costumer, Cart, CartProduct
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


def getUserCart(request):
    if request.user.is_authenticated():
        profile = request.user.get_profile()
        if profile.cart is None:
            if 'cart' in request.session:
                # cart migration from guest to registered user
                try:
                    profile.cart = Cart.objects.get(pk=request.session['cart'])
                except Cart.DoesNotExist:
                    # invalid cart. Create a new one
                    profile.cart = Cart.objects.create()
                # delete session cart because it has either been migrated or was invalid
                del request.session['cart']
            else:
                profile.cart = Cart.objects.create()
        return profile.cart
    else:
        if 'cart' in request.session:
            try:
                new_cart = Cart.objects.get(pk=request.session['cart'])
            except Cart.DoesNotExist:
                # invalid cart. Create a new one
                new_cart = Cart.objects.create()
                request.session['cart'] = new_cart.pk
        else:
            new_cart = Cart.objects.create()
            request.session['cart'] = new_cart.pk
        return new_cart


def validateAndCleanArgs(request, *args):
    if request.method != 'POST':
        return None
    ret = {}
    for var in args:
        if var[0] not in request.POST:
            return None
        try:
            ret[var[0]] = var[1](request.POST[var[0]])
        except ValueError:
            return None
    return ret


def addProductToCart(request):
    if request.user.is_staff:
        return HttpResponseRedirect('/')
    else:
        ret = validateAndCleanArgs(request, ('product_id', int), ('quantity', int))
        if ret:
            try:
                product = Product.objects.get(pk=ret['product_id'])
            except Product.DoesNotExist:
                pass
            else:
                cart = getUserCart(request)
                cart.addNumProduct(product, ret['quantity'])
        return HttpResponseRedirect('/user/cart/')


def updateProductsOnCart(request):
    if request.user.is_staff:
        return HttpResponseRedirect('/')
    else:
        if request.method == 'POST':
            cart = getUserCart(request)
            for i in request.POST:
                if not i.startswith('quantity_'):
                    continue
                try:
                    idnum = int(i[9:])
                    qntnum = int(request.POST[i])
                except ValueError as e:
                    continue
                try:
                    product = Product.objects.get(pk=idnum)
                except Product.DoesNotExist as e:
                    continue
                cart.setNumProduct(product, qntnum)
        return HttpResponseRedirect('/user/cart/')


def userCart(request, template_name='user/user_cart.html'):
    if request.user.is_staff:
        return HttpResponseRedirect('/')

    context = {'cartprods': CartProduct.objects.filter(cart=getUserCart(request))}
    return render_to_response(template_name, context, context_instance=RequestContext(request))
