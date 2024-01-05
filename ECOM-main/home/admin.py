from django.contrib import admin
from home.models import Setting, ContactMessage, FAQ
from modeltranslation.admin import TranslationAdmin
############################################################################
from product.models import Images


class SettingAdmin(admin.ModelAdmin): # home nastroyka admin paneli tugashi
    list_display = ['title', 'phone', 'create_at', 'status']
###########################################################################
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'subject', 'email', 'message', 'create_at']
    readonly_fields = ('name', 'subject', 'email', 'message', 'ip', 'phone')
    list_filter = ['status']
###########################################################################

class FAQAdmin(TranslationAdmin):
    list_display = ['question', 'answer', 'ordernumber', 'status']
    list_filter = ['status']

admin.site.register(Setting, SettingAdmin), # home admin paneliniki
admin.site.register(ContactMessage)# contact us habar kelishi
admin.site.register(FAQ, FAQAdmin)