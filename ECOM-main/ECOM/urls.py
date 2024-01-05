from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from home import views

from order import views as OrderViews
from creatoradmin import views as CreatoradminViews
from creatoradmin import views as UserViews
from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import gettext_lazy as _
urlpatterns = [
    path('selectlanguage', views.selectlanguage, name='selectlanguage'),
    path('selectlanguagess',    CreatoradminViews.selectlanguagess, name='selectlanguagess'),
    path('i18n/', include('django.conf.urls.i18n')),
]


urlpatterns += i18n_patterns (
    path('contact/',views.contactus, name='contactus'),
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('order/', include('order.urls')),
    path('shopcart/', OrderViews.shopcart, name='shopcart'),
    path('delete/<int:id>', views.delete, name='delete'),
    path('home/', include('home.urls')),
    path('', views.index, name='home'),
    path('user/', include('creatoradmin.urls')),
    path('login/', UserViews.login_form, name='login_form'),
    path('logout_form/', UserViews.logout_form, name='logout_form'),
    path('register/', UserViews.register, name='register'),
    path('developer_home/', UserViews.developer_home, name='developer_home'),
    path('startapper_home/', UserViews.startapper_home, name='startapper_home'),
    path('faq/', views.faq, name='faq'),
    path('product/', include('product.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('searchs/', views.searchs, name='searchs'),
    path('search_auto/', views.search_auto, name='search_auto'),
    path('category/<int:id>/<slug:slug>',views.category_product, name='category_product'),
    path('product/<int:id>/<slug:slug>', views.product_detail, name='product_detail'),
    prefix_default_language=False,
)

if settings.DEBUG:
    urlpatterns +=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


