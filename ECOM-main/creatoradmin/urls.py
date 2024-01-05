from django.urls import path

from . import views
from .views import product_update

urlpatterns = [
    path('category_update/', views.category_update, name ='category_update'),
    path('category_edit/<int:id>/<slug:slug>', views.category_edit, name ='category_edit'),
    path('category_delate/<int:id>/<slug:slug>', views.category_delate, name ='category_delate'),

    path('comment/', views.comment, name ='comment'),
    path('comment_delate/<int:id>', views.comment_delate, name='comment_delate'),

    path('faqs/', views.faqs, name ='faqs'),
    path('faq_update/', views.faq_update, name ='faq_update'),
    path('faq_edit/<int:id>', views.faq_edit, name='faq_edit'),
    path('faq_delate/<int:id>', views.faq_delate, name = 'faq_delate'),

    path('admin_note/<int:id>', views.admin_note, name='admin_note'),
    path('order_delate/<int:id>', views.order_delate, name='order_delate'),

    path('search/', views.search, name='search'),  # search +
    path('search_autoo/', views.search_autoo, name='search_autoo'),

    path('product_update/', views.product_update, name ='product_update'),
    path('product_edit/<int:id>/<slug:slug>', views.product_edit, name = 'product_edit'),
    path('product_delate/<int:id>/<slug:slug>', views.product_delate, name = 'product_delate'),

    path('password/', views.user_password, name='user_password'),
    path('developer_home/', views.developer_home, name='developer_home'),
    path('startapper_home/', views.startapper_home, name='startapper_home'),
    path('user-update/', views.user_update, name='user-update'),

    path('user_commentss/', views.user_commentss, name='user_commentss'),
    path('deletecomment/<int:id>', views.deletecomment, name='deletecomment'),

    path('orders_product/', views.user_orders_product, name='user_orders_product'),
    path('order_product_detail/<int:id>/<int:oid>', views.user_order_product_detail, name='user_order_product_detail'),


    path('createproduct/', views.createproduct, name='createproduct'),
    path('createcategory/', views.createcategory, name='createcategory'),

    path('orderdetail/', views.orderdetail, name='orderdetail'),
    path('user-startapper-update/', views.CreatorUpdateView.as_view(), name='CreatorUpdateView'),
    path('user-developer-update/', views.CustomerUpdateView.as_view(), name='CustomerUpdateView'),

]