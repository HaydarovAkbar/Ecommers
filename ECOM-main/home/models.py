from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models

    # home nastroykasi
from django.forms import ModelForm, TextInput, EmailInput, Textarea



class Setting(models.Model):
    STATUS =(
        ('True', 'Mavjud'),
        ('False', 'Mavjud emas'),
    )
    title = models.CharField(max_length=255)
    address = models.CharField(max_length=255, blank=True)
    phone = models.CharField(blank=True, max_length=20)
    email = models.CharField(max_length=255, blank=True)
    image = models.ImageField(blank=True,upload_to='images/')
    telegram = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=15, choices=STATUS, default='True')
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
##############################################################################
######################### Home nastroykasi madelkasi #########################
##############################################################################


class ContactMessage(models.Model):
    STATUS = (
        ('New', 'Yangi'),
        ('Read', 'Read'),
        ('Closed', 'Yopilgan'),
    )
    name = models.CharField(blank=True, max_length=20)
    email = models.CharField(blank=True, max_length=50)
    subject = models.CharField(blank=True, max_length=50)
    message = models.TextField(blank=True, max_length=255)
    phone = models.TextField(blank=True, max_length=255)
    status = models.CharField(max_length=15, choices=STATUS, default='New')
    ip = models.CharField(blank=True, max_length=50)
    note = models.CharField(blank=True, max_length=100)
    creat_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name



class ContactForm(ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name',  'subject','email','message', 'phone']
        widgets = {
            'name': TextInput(attrs={'class': 'input', 'placeholder': 'Name'}),
            'email': EmailInput(attrs={'class': 'input', 'placeholder': 'Email'}),
            'phone': TextInput(attrs={'class': 'input', 'placeholder': 'Phone'}),
            'subject': TextInput(attrs={'class': 'input', 'placeholder': 'Subject'}),
            'message': Textarea(attrs={'class': 'input', 'placeholder': 'Your message', 'rows':'5'}),
        }
################################################################################################################
################################################################################################################
class FAQ(models.Model):
    STATUS = (
        ('True', 'Mavjud'),
        ('False','Yopilgan'),
    )
    ordernumber = models.IntegerField()
    question = models.CharField(max_length=1000)
    answer = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS,)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.question


