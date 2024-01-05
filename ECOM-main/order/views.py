import profile

from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.utils.crypto import get_random_string

from home.models import Setting
from order.models import ShopCart, ShopCartForm, OrderForm, Order, OrderProduct
from product.models import Category, Product, Images, Comment
from creatoradmin.models import Customer


def index(request):
    return HttpResponse('Order Page')


@login_required(login_url='login')  # Check login
def addtoshopcart(request, id):
    url = request.META.get('HTTP_REFERER')  # get last url
    current_user = request.user  # Access User Session information

    checkproduct = ShopCart.objects.filter(product_id=id)  # Check product in shopcart
    if checkproduct:
        control = 1  # The product is in the cart
    else:
        control = 0  # The product is not in the cart

    if request.method == 'POST':  # if there is a post
        form = ShopCartForm(request.POST)
        if form.is_valid():
            if control == 1:  # Update shopcart
                data = ShopCart.objects.get(product_id=id)
                data.quantity += form.cleaned_data['quantity']
                data.save()
            else:  # Insert to Shopcart
                data = ShopCart()
                data.user_id = current_user.id
                data.product_id = id
                data.quantity = form.cleaned_data['quantity']
                data.save()
        messages.success(request, "Product added to ShopCart")
        return HttpResponseRedirect(url)
    else:  # if there is no post
        if control == 1:  # Update shopcart
            data = ShopCart.objects.get(product_id=id)
            data.quantity += 1
            data.save()  #
        else:  # Insert to shopcart
            data = ShopCart()  # model
            data.user_id = current_user.id
            data.product_id = id
            data.quantity = 1
            data.save()  #
        messages.success(request, "Product added to ShopCart")
        return HttpResponseRedirect(url)


def shopcart(request):
    category = Category.objects.all()
    setting = Setting.objects.all()
    current_user = request.user
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    total = 0
    total_qty = 0
    for rs in shopcart:
        total_qty += rs.quantity
        total += rs.product.price * rs.quantity
    # return HttpResponse(str(total))
    context = {
        'shopcart': shopcart,
        'category': category,
        'total': total,
        'total_qty': total_qty,
        'setting': setting,

    }
    return render(request, 'shopcart.html', context)


@login_required(login_url='/login')  # check login
def deletefromcart(request, id):
    ShopCart.objects.filter(id=id).delete()
    messages.success(request, "Your item deleted from Shop Cart!")
    return HttpResponseRedirect("/shopcart")


###################################################################################################################
###################################################################################################################
###################################################################################################################
def orderproduct(request):
    category = Category.objects.all()
    setting = Setting.objects.all()
    current_user = request.user
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    profile = Customer.objects.get(user_id=current_user.id)

    total_quantity = 0
    total = 0
    for rs in shopcart:
        total += rs.product.price * rs.quantity
        total_quantity += rs.quantity
    # return HttpResponse(str(total))

    if request.method == 'POST':  # if there is a post
        form = OrderForm(request.POST)
        if form.is_valid():
            data = Order()
            data.first_name = form.cleaned_data['first_name']  # get product quantity from form
            data.last_name = form.cleaned_data['last_name']
            data.address = form.cleaned_data['address']
            data.phone = form.cleaned_data['phone']
            data.country = form.cleaned_data['country']
            data.city = form.cleaned_data['city']
            data.user_id = current_user.id
            data.total = total
            data.total_quantity = total_quantity
            data.ip = request.META.get('REMOTE_ADDR')
            ordercode = get_random_string(12).upper()  # random code
            data.code = ordercode
            data.save()

            # Move Shopcart items to Order Product items
            shopcart = ShopCart.objects.filter(user_id=current_user.id)
            for rs in shopcart:
                detail = OrderProduct()
                detail.order_id = data.id  # Order id
                detail.product_id = rs.product_id
                detail.user_id = current_user.id
                detail.quantity = rs.quantity
                detail.price = rs.product.price
                detail.amount = rs.amount
                detail.save()
                # Reduce quantity of sold product from Amount of Product
                product = Product.objects.get(id=rs.product_id)
                product.amount -= rs.quantity
                product.save()

            ShopCart.objects.filter(user_id=current_user.id).delete()
            request.session['cart_items'] = 0
            messages.success(request, "Your Order Has Been Completed! Thank you!")
            return render(request, 'ordercomplete.html', {'ordercode': ordercode,
                                                          'category': category,
                                                          'total': total,
                                                          'total_quantity': total_quantity,
                                                          'profile': profile,
                                                          'shopcart': shopcart,
                                                          'setting': setting})
        else:
            messages.warning(request, form.errors)
            return HttpResponseRedirect("/order/orderproduct")

    form = OrderForm
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    profile = Customer.objects.get(user_id=current_user.id)
    setting = Setting.objects.all()
    context = {
        'shopcart': shopcart,
        'category': category,
        'total': total,
        'total_quantity': total_quantity,
        'profile': profile,
        'form': form,
        'setting': setting

    }

    return render(request, 'orderproduct.html', context)
