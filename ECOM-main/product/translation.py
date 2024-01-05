from modeltranslation.translator import register, TranslationOptions
from product.models import Category, Product


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('title',)


@register(Product)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('title', 'description',)