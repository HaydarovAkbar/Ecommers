from modeltranslation.translator import register, TranslationOptions
from home.models import FAQ


@register(FAQ)
class FaqTranslationOptions(TranslationOptions):
    fields = ('question', 'answer',)
