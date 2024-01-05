import json
from django.shortcuts import render, HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.crypto import get_random_string
from django.utils import translation
from home.models import Setting, ContactMessage, FAQ
from order.models import Order, ShopCart, OrderProduct
from product.models import Product, Category, Comment
from .models import CustomUser, Creator, Customer
from creatoradmin.forms import UserUpdateForm, StartapperUpdateForm, StaffUpdateForm, RegisterForm, AddProductForm, \
    AddCategoryForm, EditProduct, CategoryEdit, AdminNoteForm, SearchForm, FaqForm, FaqEditForm
from django.views import View


def home(request):
    return render(request, 'index.html')


### RO'YHATDAN O'TISH
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            user.save()
            login(request, user)
            current_user = CustomUser.objects.get(email=request.user.email)
            if current_user.user_type == CustomUser.Customer:
                Customer.objects.create(user=user)
                messages.success(request, 'Your account has been created')
                return redirect('home')
        else:
            messages.warning(request, "Registration error!")
            return HttpResponseRedirect('/')
    form = RegisterForm()
    return render(request, 'signup_form.html', {'form': form})


#################################################################################################################
#################################################################################################################
#################################################################################################################
# KIRISH
def login_form(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return HttpResponseRedirect('/')
        else:
            messages.warning(request, 'Error!')
            return redirect('login')
    return render(request, 'login.html')


#################################################################################################################
#################################################################################################################
#################################################################################################################
## CHIQISH
def logout_form(request):
    logout(request)
    return HttpResponseRedirect('/')


#################################################################################################################
#################################################################################################################
#################################################################################################################
## USER PAGE
@login_required(login_url='login')
def developer_home(request):
    try:
        user = Customer.objects.get(user=request.user)
    except:
        messages.warning(request, 'you go to developer page')
        return redirect('home')

    context = {
        'user': user,
    }
    return render(request, 'developer_home.html', context)


#################################################################################################################
#################################################################################################################
#################################################################################################################
## ADMIN PAGE
@login_required(login_url='login')
def startapper_home(request):
    try:
        admin = Creator.objects.get(user=request.user)
    except:
        messages.warning(request, 'you go to developer page')
        return redirect('home')
    customer = Customer.objects.all()
    customer_count = customer.count()
    products = Product.objects.all()
    products_count = products.count()
    categories = Category.objects.all()
    categories_count = categories.count
    orders = Order.objects.all()
    orders_count = orders.count()
    setting = Setting.objects.all()
    productlist = Product.objects.all().order_by('id')
    productcategory = Category.objects.all().order_by('id')
    customere = Customer.objects.all().order_by('id')
    shop = ShopCart.objects.all().order_by('id')
    customer_user = request.user
    order = OrderProduct.objects.all()
    orderdetail = Order.objects.all()
    contact = ContactMessage.objects.all().order_by('id')
    contact_count = contact.count()
    comment = Comment.objects.all().order_by('id')
    comment_count = comment.count()
    context = {
        'admin': admin,
        'customer': customer,
        'customer_count': customer_count,
        'products_count': products_count,
        'categories_count': categories_count,
        'orders_count': orders_count,
        'contact_count':contact_count,

        'setting': setting,
        'productlist': productlist,
        'productcategory': productcategory,
        'customer_user': customer_user,
        'customeree': customere,
        'order': order,
        'orderdetail': orderdetail,
        'shop': shop,
        'contact':contact,
        'comment_count':comment_count,

    }
    return render(request, 'startapper_home.html', context)


#################################################################################################################
#################################################################################################################
#################################################################################################################
## UPDATE
@login_required(login_url='/login')
def user_update(request):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'You profile successfully updated!')
            return HttpResponseRedirect(url)
    else:
        form = UserUpdateForm(instance=request.user)
        return render(request, 'user_update.html', {'form': form})


#################################################################################################################
#################################################################################################################
#################################################################################################################

@login_required(login_url='/login')
def user_password(request):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your profile password successfully updated')
            return redirect(url)
        else:
            messages.error(request, 'Eror password')
            return redirect('startapper_home')
    else:
        form = PasswordChangeForm(request.user)
        return render(request, 'user_password.html', {'form': form})


class CreatorUpdateView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        startapper = Creator.objects.get(user=self.request.user)
        form = StartapperUpdateForm(instance=startapper)
        context = {'form': form}
        return render(request, 'profile_update.html', context)

    def post(self, *args, **kwargs):
        form = StartapperUpdateForm(self.request.POST, self.request.FILES, instance=self.request.user.creator)
        if form.is_valid():
            form.save()
            return redirect(reverse('startapper_home'))
        return redirect('home')


class CustomerUpdateView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        staff = Customer.objects.get(user=self.request.user)
        form = StaffUpdateForm(instance=staff)
        context = {'form': form}
        return render(request, 'profile_update_staff.html', context)

    def post(self, *args, **kwargs):
        form = StaffUpdateForm(self.request.POST, self.request.FILES, instance=self.request.user.customer)
        if form.is_valid():
            form.save()
            return redirect(reverse('developer_home'))
        return redirect('home')


def createproduct(request):
    if request.method == 'POST':
        form = AddProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = Product()
            product.title_uz = form.cleaned_data.get('title_uz')
            product.title_en = form.cleaned_data.get('title_en')
            product.title_ru = form.cleaned_data.get('title_ru')
            product.price = form.cleaned_data.get('price')
            product.description_uz = form.cleaned_data.get('description_uz')
            product.description_en = form.cleaned_data.get('description_en')
            product.description_ru = form.cleaned_data.get('description_ru')
            product.category = form.cleaned_data.get('category')
            if request.FILES:
                product.image = request.FILES['image']
            product.amount = form.cleaned_data.get('amount')
            product.minamount = form.cleaned_data.get('minamount')
            product.slug = form.cleaned_data.get('slug')
            product.status = form.cleaned_data.get('status')
            product.save()
            return redirect('startapper_home')
    form = AddProductForm()
    admin = Creator.objects.get(user=request.user)
    context = {
        'form': form,
        'admin': admin,
    }
    return render(request, 'add_product.html', context)


def createcategory(request):
    if request.method == 'POST':
        form = AddCategoryForm(request.POST, request.FILES)
        if form.is_valid():
            category = Category()
            category.title_uz = form.cleaned_data.get('title_uz')
            category.title_en = form.cleaned_data.get('title_en')
            category.title_ru = form.cleaned_data.get('title_ru')
            category.description = form.cleaned_data.get('description')
            if request.FILES:
                category.image = request.FILES['image']
            category.slug = form.cleaned_data.get('slug')
            category.status = form.cleaned_data.get('status')
            category.save()
            return redirect('startapper_home')
    form = AddCategoryForm()
    admin = Creator.objects.get(user=request.user)
    context = {
        'form': form,
        'admin': admin,
    }
    return render(request, 'add_category.html', context)


def orderdetail(request):
    setting = Setting.objects.all().order_by('id')
    productlist = Product.objects.all().order_by('id')
    productcategory = Category.objects.all().order_by('id')
    customer = Customer.objects.all().order_by('id')
    shop = ShopCart.objects.all().order_by('id')
    customer_user = request.user
    order = OrderProduct.objects.all().order_by('id')
    orderdetail = Order.objects.all().order_by('id')
    admin = Creator.objects.get(user=request.user)
    context = {

        'setting': setting,
        'productlist': productlist,
        'productcategory': productcategory,
        'customer_user': customer_user,
        'customer': customer,
        'order': order,
        'orderdetail': orderdetail,
        'shop': shop,
        'admin': admin,
    }
    return render(request, 'orderlist.html', context)

def admin_note(request, id):
    order = Order.objects.get(pk=id)
    customer = Customer.objects.all().order_by('id')
    admin = Creator.objects.get(user=request.user)
    if request.method == 'POST':
        form = AdminNoteForm(request.POST,  instance=order)
        if form.is_valid():
            form.save()
            return redirect('startapper_home')
    else:
        form = AdminNoteForm(instance=order)
        context = {'form': form,
                'admin': admin,
                'order':order,
                'customer':customer,
                   }

        return render(request, 'admin_note.html', context)

def order_delate(request, id):
    orders = Order.objects.get(pk=id)
    orders.delete()
    return redirect('startapper_home')



def category_update(request):
    category = Category.objects.all().order_by('id')
    admin = Creator.objects.get(user=request.user)
    context = {
        'category': category,
        'admin': admin,
    }

    return render(request, 'category_update.html', context)

def category_edit(request, id, slug):
    category = Category.objects.get(pk=id)
    admin = Creator.objects.get(user=request.user)
    if request.method == 'POST':
        form = CategoryEdit(request.POST, request.FILES, instance=category)
        if request.FILES:
            category.image = request.FILES['image']
        if form.is_valid():
            form.save()
            return redirect('category_update')
    else:
        form = CategoryEdit(instance=category)
        context = {'form': form,
                'admin': admin}

        return render(request, 'category_edit.html', context)


def category_delate(request, id, slug):
    category = Category.objects.get(pk=id)
    category.delete()
    return redirect('startapper_home')





def product_update(request):
    product = Product.objects.all().order_by('id')
    admin = Creator.objects.get(user=request.user)
    context = {
        'product': product,
        'admin': admin,
    }

    return render(request, 'product_update.html', context)



def product_edit(request, id, slug):
    admin = Creator.objects.get(user=request.user)
    product = Product.objects.get(pk=id)
    if request.method == 'POST':
        form = EditProduct(request.POST, request.FILES, instance=product)
        if request.FILES:
            product.image = request.FILES['image']
        if form.is_valid():
            form.save()
            return redirect('product_update')
    else:
        form = EditProduct(instance=product)
        context = {'form': form,
                   'admin':admin,}

        return render(request, 'product_edit.html', context)


def product_delate(request, id, slug):
    product = Product.objects.get(pk=id)
    product.delete()
    return redirect('startapper_home')



def search(request):
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

            context = {
                'products': products,
                'query': query,
                'category': category,
                'setting' : setting,

            }
            return render(request, 'search.html', context)
    return HttpResponseRedirect('/')


def search_autoo(request):
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


def comment(request):
    product = Product.objects.all().order_by('id')
    customer = Customer.objects.all().order_by('id')
    comment = Comment.objects.all().order_by('id')
    admin = Creator.objects.get(user=request.user)
    context = {
        'product':product,
        'customer': customer,
        'comment':comment,
        'admin':admin,
    }
    return render(request, 'comment.html', context)


def comment_delate(request, id,):
    comments = Comment.objects.get(pk=id)
    comments.delete()
    return redirect('comment')


def faqs(request):
    if request.method == 'POST':
        form = FaqForm(request.POST)
        if form.is_valid():
            faq = FAQ()
            faq.ordernumber = form.cleaned_data.get('ordernumber')
            faq.question_uz = form.cleaned_data.get('question_uz')
            faq.question_en = form.cleaned_data.get('question_en')
            faq.question_ru = form.cleaned_data.get('question_ru')
            faq.answer_uz = form.cleaned_data.get('answer_uz')
            faq.answer_en = form.cleaned_data.get('answer_en')
            faq.answer_ru = form.cleaned_data.get('answer_ru')

            faq.status = form.cleaned_data.get('status')
            faq.save()
            return redirect('startapper_home')
    form = FaqForm()
    admin = Creator.objects.get(user=request.user)
    context = {
        'form': form,
        'admin': admin,
    }
    return render(request, 'faqs.html', context)


def faq_update(request):
    faq = FAQ.objects.all().order_by('id')
    admin = Creator.objects.get(user=request.user)
    context = {
        'faq': faq,
        'admin': admin,
    }

    return render(request, 'faq_update.html', context)

def faq_edit(request, id):
    admin = Creator.objects.get(user=request.user)
    faqss = FAQ.objects.get(pk=id)
    if request.method == 'POST':
        form = FaqEditForm(request.POST, instance=faqss)
        if form.is_valid():
            form.save()
            return redirect('faq_update')
    else:
        form = FaqEditForm(instance=faqss)
        context = {'form': form,
                   'admin':admin,}

        return render(request, 'faq_edit.html', context)


def faq_delate(request, id,):
    faqsss = FAQ.objects.get(pk=id)
    faqsss.delete()
    return redirect('faq_update')






def user_commentss(request):
    category = Category.objects.all()
    setting = Setting.objects.all()
    current_user = request.user
    comments = Comment.objects.filter(user_id=current_user.id)
    current_user = request.user
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    order = Order.objects.all()
    total = 0
    total_qty = 0
    for rs in shopcart:
        total_qty += rs.quantity
        total += rs.product.price * rs.quantity
    context = {'category': category,
               'comments': comments,
               'setting': setting,
               'shopcart': shopcart,
               'order': order,
               'total': total,
               'total_qty': total_qty,
               }
    return render(request, 'user_comments.html', context)


def deletecomment(request,id):
    current_user = request.user
    Comment.objects.filter(id=id, user_id=current_user.id).delete()
    messages.success(request, "Comment has been deleted!")
    return redirect("user_commentss")


def user_orders_product(request):
    category = Category.objects.all()
    setting = Setting.objects.all()
    current_user = request.user
    order_product = OrderProduct.objects.filter(user_id=current_user.id)
    current_user = request.user
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    order = Order.objects.all()
    total = 0
    total_qty = 0
    for rs in shopcart:
        total_qty += rs.quantity
        total += rs.product.price * rs.quantity


    context = { 'category': category,
                'order_product': order_product,
                'setting' : setting,
                'shopcart': shopcart,
                'order': order,
                'total': total,
                'total_qty': total_qty,
    }
    return render(request, 'user_order_product.html', context)


def user_order_product_detail(request,id, oid):
    category = Category.objects.all()
    setting = Setting.objects.all()
    current_user = request.user
    order = Order.objects.get(user_id=current_user.id, id=oid)
    orderitem = OrderProduct.objects.filter(id=id,user_id=current_user.id)
    current_user = request.user
    shopcart = ShopCart.objects.filter(user_id=current_user.id)

    total = 0
    total_qty = 0
    for rs in shopcart:
        total_qty += rs.quantity
        total += rs.product.price * rs.quantity

    context = { 'category': category,

                'orderitem': orderitem,
                'setting' : setting,
                'shopcart': shopcart,
                'order': order,
                'total': total,
                'total_qty': total_qty,
    }
    return render(request, 'user_order_product_detail.html', context)




def selectlanguagess(request):
    if request.method == 'POST':  # check post
        cur_language = translation.get_language()
        lasturl= request.META.get('HTTP_REFERER')
        lang = request.POST['language']
        translation.activate(lang)
        request.session[translation.LANGUAGE_SESSION_KEY]=lang
        #return HttpResponse(lang)
        return redirect('startapper_home')