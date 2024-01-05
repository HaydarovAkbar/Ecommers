from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from modeltranslation.forms import TranslationModelForm
from home.models import FAQ
from order.models import Order
from product.models import Product, Category
from .models import CustomUser, Creator, Customer


class RegisterForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ['username', 'full_name', 'phone', 'password1', 'password2', 'email', 'user_type']

        widgets = {
            'user_type': forms.Select(
                attrs={'class': "form-control"}
            )
        }


class UserUpdateForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'full_name', 'phone',)
        # widgets = {'user_type': forms.Select(attrs={'class': "form-control"})}


class StartapperUpdateForm(forms.ModelForm):
    class Meta:
        model = Creator
        fields = ['bio', 'country', 'address', 'city', 'image']


class StaffUpdateForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['bio', 'country', 'address', 'city', 'image']



class AddProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title_uz','title_en','title_ru',  'description_uz','description_en','description_ru', 'price', 'amount', 'minamount', 'image', 'category', 'slug', 'status']


class AddCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = [ 'title_uz', 'title_en', 'title_ru', 'description', 'image',  'slug', 'status']


class EditProduct(forms.ModelForm):
    class Meta:
        model = Product
        fields = ( 'title_uz', 'title_en', 'title_ru', 'price',  'description_uz', 'description_en', 'description_ru',  'category', 'image', 'amount', 'minamount', 'status', 'slug',)


class CategoryEdit(forms.ModelForm):
    class Meta:
        model = Category
        fields = ( 'title_uz', 'title_en', 'title_ru', 'description',   'image', 'status', 'slug',)

class AdminNoteForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('adminnote', 'status','user',  'country', 'city', 'phone', 'address', 'total', 'first_name', 'last_name','ip',)


class SearchForm(forms.Form):
    query = forms.CharField(max_length=100)
    catid = forms.IntegerField()

class FaqForm(forms.ModelForm):
    class Meta:
        model = FAQ
        fields = ('ordernumber',  'question_uz', 'question_en', 'question_ru',  'answer_uz', 'answer_en', 'answer_ru', 'status',)


class FaqEditForm(forms.ModelForm):
    class Meta:
        model = FAQ
        fields = ('ordernumber', 'question_uz', 'question_en', 'question_ru', 'answer_uz', 'answer_en', 'answer_ru', 'status',)