from django.contrib import admin
from parler.admin import TranslatableAdmin

from .models import *

admin.site.register(Creator)
admin.site.register(Customer)
admin.site.register(CustomUser)








