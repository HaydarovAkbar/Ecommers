from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django.db import models
from django.db.models import Avg, Count
from django.forms import ModelForm
from django.urls import reverse
from django.utils.safestring import mark_safe
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel

########################################################################################################################
########################################################################################################################
########################################################################################################################
from creatoradmin.models import CustomUser


class Category(MPTTModel):
    STATUS = (
        ('True', 'Mavjud'),
        ('False', 'Mavjud Emas'),
    )
    parent = TreeForeignKey('self',
                            blank=True,
                            null=True,
                            related_name='children',
                            on_delete=models.CASCADE)
    title = models.CharField(max_length=50)

    description = models.CharField(max_length=255)
    image = models.ImageField(blank=True, upload_to='images/')
    status = models.CharField(max_length=15, choices=STATUS)
    slug = models.SlugField(null=False, unique=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class MPTTMeta:
    order_insertion_by = ['title']

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'self': self.slug})

    def __str__(self):
        full_path = [self.title]
        k = self.parent
        while k is not None:
            full_path.append(k.title)
            k = k.parent
        return '/'.join(full_path[::-1])


########################################################################################################################
########################################################################################################################
########################################################################################################################
class Product(models.Model):
    STATUS = (
        ('True', 'Mavjud'),
        ('False', 'Mavjud Emas'),
    )
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, unique=True, )
    description = models.TextField(blank=True)
    image = models.ImageField(blank=True, upload_to='images/')
    price = models.FloatField()
    amount = models.IntegerField()
    minamount = models.IntegerField()
    status = models.CharField(max_length=15, choices=STATUS)
    slug = models.SlugField(null=False, unique=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))

    image_tag.short_description = 'Image'

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'self': self.slug})

    def avaregereview(self):
        reviews = Comment.objects.filter(product=self, status='True').aggregate(avarage=Avg('rate'))
        avg = 0
        if reviews["avarage"] is not None:
            avg = float(reviews["avarage"])
        return avg

    def countreview(self):
        reviews = Comment.objects.filter(product=self, status='True').aggregate(count=Count('id'))
        cnt = 0
        if reviews["count"] is not None:
            cnt = int(reviews["count"])
        return cnt


class Images(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, blank=True)
    image = models.ImageField(blank=True, upload_to='images/')

    def __str__(self):
        return self.title


###############################################################################################################
################################ Category bilan product madelkasi #############################################
###############################################################################################################

##############################################################################################################
##############################################################################################################
##############################################################################################################

class Comment(models.Model):
    STATUS = (
        ('True', 'Mavjud'),
        ('False', 'Mavjud Emas'),
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    subject = models.CharField(max_length=55, blank=True)
    comment = models.TextField(max_length=255, blank=True)
    rate = models.IntegerField(default=1)
    ip = models.CharField(max_length=20, blank=True)
    status = models.CharField(max_length=15, choices=STATUS, default='True')
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['subject', 'comment', 'rate']
########################################################################################################################
########################################################################################################################
########################################################################################################################
