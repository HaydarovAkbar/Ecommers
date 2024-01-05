import json

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, HttpResponse
from django.core.paginator import (Paginator, PageNotAnInteger, EmptyPage)
# Create your views here.
from django.utils import translation
from home.models import Setting, ContactForm, ContactMessage, FAQ
from home.forms import SearchForm
from order.models import ShopCart, Order
from product.models import Category, Product, Images,  Comment


def index(request):
    setting = Setting.objects.all()
    category = Category.objects.all()
    product_slider = Product.objects.all().order_by('id')[:5]
    product_latest = Product.objects.all().order_by('-id')
    product_picked = Product.objects.all().order_by('?')[:8]
    current_user = request.user
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    order = Order.objects.all()
    total = 0
    total_qty = 0
    for rs in shopcart:
        total_qty += rs.quantity
        total += rs.product.price * rs.quantity
    page = "home"
    context = {

        'setting': setting,
        'category': category,
        'product_slider': product_slider,
        'product_latest':product_latest,
        'product_picked': product_picked,
        'page': page,
        'shopcart':shopcart,
        'order':order,
        'total': total,
        'total_qty': total_qty,

    }
    return render(request,'index.html', context)

def delete(request, id):
    ShopCart.objects.filter(id=id).delete()
    messages.success(request, "Your item deleted from Shop Cart!")
    return HttpResponseRedirect("/")



def aboutus(request):
    setting = Setting.objects.all()
    context = {'setting': setting,}
    return render(request, 'about-us.html', context)


def contactus(request):
    if request.method =='POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            data = ContactMessage()
            data.name = form.cleaned_data['name']
            data.email = form.cleaned_data['email']
            data.subject = form.cleaned_data['subject']
            data.message = form.cleaned_data['message']
            data.phone = form.cleaned_data['phone']
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            messages.success(request, "Sizning xabaringiz yuborildi! Rahmat")
            return HttpResponseRedirect('/contact')
    setting = Setting.objects.all()
    current_user = request.user
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    order = Order.objects.all()
    total = 0
    total_qty = 0
    for rs in shopcart:
        total_qty += rs.quantity
        total += rs.product.price * rs.quantity
    form = ContactForm
    context = {'setting': setting,
               'form': form,
               'shopcart': shopcart,
               'order': order,
               'total': total,
               'total_qty': total_qty,
               }
    return render(request,'contact.html', context)







def category_product(request,id, slug):
    category = Category.objects.all()
    setting = Setting.objects.all()
    product_slider = Product.objects.all().order_by('?')[:8]
    product_picked = Product.objects.all().order_by('id')[:8]
    product_latest = Product.objects.all().order_by('-id')[:8]
    catdata = Category.objects.get(pk=1)
    products = Product.objects.filter(category_id=id)
    paginator = Paginator(products, 9)
    page_request_var = 'page'
    page = request.GET.get(page_request_var)
    current_user = request.user
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    order = Order.objects.all()
    total = 0
    total_qty = 0
    for rs in shopcart:
        total_qty += rs.quantity
        total += rs.product.price * rs.quantity

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    context = {
        'category': category,
        'catdata': catdata,
        'products': products,
        'setting' : setting,
        'product_latest' : product_latest,
        'product_picked' : product_picked,
        'product_slider' : product_slider,
        'shopcart': shopcart,
        'order': order,
        'total': total,
        'total_qty': total_qty,
    }
    return render(request, 'category_detail.html', context)

########################################################################################################################
########################################################################################################################


########################################################################################################################
########################################################################################################################
def product_detail(request, id, slug):
    category = Category.objects.all()
    setting = Setting.objects.all()
    product_picked = Product.objects.all().order_by('?')[:8]
    product_latest = Product.objects.all().order_by('-id')[:8]
    product = Product.objects.get(pk=id)
    images = Images.objects.filter(product_id=id)
    comments = Comment.objects.filter(product_id=id, status='True')
    current_user = request.user
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    order = Order.objects.all()
    total = 0
    total_qty = 0
    for rs in shopcart:
        total_qty += rs.quantity
        total += rs.product.price * rs.quantity
    context = {
        'category': category,
        'product': product,
        'images': images,
        'comments': comments,
        'setting' : setting,
        'product_latest' : product_latest,
        'product_picked' : product_picked,
        'shopcart': shopcart,
        'order': order,
        'total': total,
        'total_qty': total_qty,
    }
    return render(request, 'product_detail.html', context)
#####################################################################################################################
#####################################################################################################################
#####################################################################################################################

def searchs(request):
    if request.method=='POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']
            catid = form.cleaned_data['catid']
            if catid == 0:
                products = Product.objects.filter(title__icontains=query)
            else:
                products = Product.objects.filter(title__icontains=query, category_id=catid)

            category = Category.objects.all()
            setting = Setting.objects.all()
            current_user = request.user
            shopcart = ShopCart.objects.filter(user_id=current_user.id)
            order = Order.objects.all()
            total = 0
            total_qty = 0
            for rs in shopcart:
                total_qty += rs.quantity
                total += rs.product.price * rs.quantity

            context = {
                'products': products,
                'query': query,
                'category': category,
                'setting' : setting,
                'shopcart': shopcart,
                'order': order,
                'total': total,
                'total_qty': total_qty,
            }
            return render(request, 'searchs.html', context)
    return HttpResponseRedirect('/')


def search_auto(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        products = Product.objects.filter(title__icontains=q)
        results = []
        for rs in products:
            products_json = {}
            products_json = rs.title
            results.append(products_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)



def faq(request):
    category = Category.objects.all()
    setting = Setting.objects.all()
    current_user = request.user
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    order = Order.objects.all()
    total = 0
    total_qty = 0
    for rs in shopcart:
        total_qty += rs.quantity
        total += rs.product.price * rs.quantity

    faq = FAQ.objects.filter(status='True').order_by('ordernumber')
    context = {'category': category,
                'faq': faq,
                'setting': setting,
                'shopcart': shopcart,
                'order': order,
                'total': total,
                'total_qty': total_qty,
                }
    return render(request, 'faq.html', context)


def selectlanguage(request):
    if request.method == 'POST':  # check post
        cur_language = translation.get_language()
        lasturl= request.META.get('HTTP_REFERER')
        lang = request.POST['language']
        translation.activate(lang)
        request.session[translation.LANGUAGE_SESSION_KEY]=lang
        #return HttpResponse(lang)
        return HttpResponseRedirect("/"+lang)

