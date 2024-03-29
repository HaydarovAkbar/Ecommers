from django.contrib import admin
from product.models import Category, Product, Images, Comment
from mptt.admin import DraggableMPTTAdmin
from modeltranslation.admin import TranslationAdmin
# Register your models here.

class CategoryAdmin(TranslationAdmin):
    list_display = ['title', 'parent', 'status']
    list_filter = ['title']
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
class CategoryAdmin2(DraggableMPTTAdmin):
    mptt_indent_field = "title"
    list_display = ('tree_actions', 'indented_title',
                    'related_products_count', 'related_products_cumulative_count')
    list_display_links = ('indented_title',)
    prepopulated_fields = {'slug':('title',)}
    def get_queryset(self, request):
        qs = super().get_queryset(request)

        qs = Category.objects.add_related_count(
            qs,
            Product,
            'category',
            'products_cumulative_count',
            cumulative=True
        )

        qs = Category.objects.add_related_count(
            qs,
            Product,
            'category',
            'products_count',
            cumulative=False
        )
        return qs
    def related_products_count(self, instance):
        return instance.products_count
    related_products_count.short_description = 'Related products (for this specific category)'
    def related_products_cumulative_count(self,instance):
        return instance.products_cumulative_count
    related_products_cumulative_count.short_description = 'Related products (in tree)'
########################################################################################################################
########################################################################################################################
########################################################################################################################

class ProductImageInline(admin.TabularInline):
    model = Images
    extra = 5
########################################################################################################################
########################################################################################################################
########################################################################################################################


class ProductAdmin(TranslationAdmin):
    list_display = ['title', 'category', 'status', 'image_tag', 'amount', 'price']
    list_filter = ['category']
    readonly_fields = ('image_tag',)
    inlines = [ProductImageInline]
    prepopulated_fields = {'slug': ('title',)}

########################################################################################################################
########################################################################################################################
########################################################################################################################
class CommentAdmin(admin.ModelAdmin):
    list_display = ['subject', 'comment', 'status', 'create_at']
    list_filter = ['status']
    readonly_fields = ('subject', 'comment', 'ip', 'user', 'product', 'rate')



admin.site.register(Category, CategoryAdmin2)
admin.site.register(Product, ProductAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Images)
