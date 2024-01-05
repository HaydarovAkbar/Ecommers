from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils import timezone
from parler.models import TranslatableModel


class CustomUser(AbstractUser):
    Creator = "Creator"
    Customer = "Customer"


    USER_TYPE = [
        (Creator, 'Creator'),
        (Customer, 'Customer'),

    ]
    full_name = models.CharField('full name', max_length=200, blank=False, null=False)
    email = models.EmailField('email address', blank=False, null=False, unique=True)
    user_type = models.CharField(max_length=30, choices=USER_TYPE)
    phone = models.CharField(max_length=30, blank=False, null=False, unique=True)
    date_joined = models.DateTimeField('date joined', default=timezone.now)
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        'username',
        max_length=150,
        unique=True,
        null=True,
        help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.',
        validators=[username_validator],
        error_messages={
            'unique': "A user with that username already exists.",
        },
    )

    def __str__(self):
        return f"{self.full_name}" or f"{self.username} this is admin"

Tashkent = 'Tashkent viloyati'
Andijon = 'Andijon viloyati'
Fargona = "Fargʻona viloyati"
Jizzax = 'Jizzax viloyati'
Samarqand = 'Samarqand viloyati'
Namangan = 'Namangan viloyati'
Navoiy = 'Navoiy viloyati'
Qashqadaryo = 'Qashqadaryo viloyati'
Sirdaryo = 'Sirdaryo viloyati'
Surxondaryo = 'Surxondaryo viloyati'
Buxoro = 'Buxoro viloyati'
Xorazm = 'Xorazm viloyati'
Qoraqalpogiston = "Qoraqalpogʻiston Respublikasi"


CITY = [
    (Tashkent, 'Tashkent viloyati'),
    (Andijon, 'Andijon viloyati'),
    (Fargona, 'Fargona viloyati'),
    (Jizzax, 'Jizzax viloyati'),
    (Samarqand, 'Samarqand viloyati'),
    (Namangan, 'Namangan viloyati'),
    (Navoiy, 'Navoiy viloyati'),
    (Qashqadaryo, 'Qashqadaryo viloyati'),
    (Sirdaryo, 'Sirdaryo viloyati'),
    (Surxondaryo, 'Surxondaryo viloyati'),
    (Buxoro, 'Buxoro viloyati'),
    (Xorazm, 'Xorazm viloyati'),
    (Qoraqalpogiston, 'Qoraqalpogiston Respublikasi'),
]

Uzbekistan = 'Uzbekistan'
# Kazahistan = 'Kazahistan'
# Armenia = 'Armenia'
# Azerbaijan = 'Azerbaijan'
# Belarus = 'Belarus'
# Georgia = 'Georgia'
# Moldova = 'Moldova'
# Russia = 'Russia'
# Ukraine = 'Ukraine'
# Norway = 'Norway'
# Turkey = 'Turkey'
# Germany = 'Germany'
# Switzerland = 'Switzerland'
# France = 'France'
# Italy = 'Italy'
# Latvia = 'Latvia'
# Slovakia = 'Slovakia'
# Spain = 'Spain'
# Sweden = 'Sweden'
# Denmark = 'Denmark'



COUNTRY = [
    (Uzbekistan,  'Uzbekistan'),
    # (Kazahistan,  'Kazahistan'),
    # (Armenia,  'Armenia'),
    # (Azerbaijan,  'Azerbaijan'),
    # (Belarus,  'Belarus'),
    # (Georgia,  'Georgia'),
    # (Moldova,  'Moldova'),
    # (Russia,  'Russia'),
    # (Ukraine,  'Ukraine'),
    # (Norway,  'Norway'),
    # (Turkey,  'Turkey'),
    # (Germany,  'Germany'),
    # (Switzerland,  'Switzerland'),
    # (France,  'France'),
    # (Italy,  'Uzbekistan'),
    # (Latvia,  'Latvia'),
    # (Slovakia,  'Slovakia'),
    # (Spain,  'Spain'),
    # (Sweden,  'Sweden'),
    # (Denmark,  'Denmark'),
]


class Creator(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    bio = models.TextField(default="no bio...", max_length=400)
    address = models.CharField(blank=True, max_length=255)
    city = models.CharField(blank=True, max_length=255, null=True, choices=CITY)
    country = models.CharField(max_length=50, blank=True, null=True, choices=COUNTRY)
    image = models.ImageField(upload_to='startapper_file/startapp_image', blank=True,)

    related = 'Creator'

    def __str__(self):
        return self.user.username


class Customer(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    bio = models.TextField(default="no bio...", max_length=400)
    address = models.CharField(blank=True, max_length=255)
    city = models.CharField(blank=True, max_length=255, null=True, choices=CITY)
    country = models.CharField(max_length=50, blank=True, null=True, choices=COUNTRY)
    image = models.ImageField(upload_to='staff_image', blank=True, null=True)

    related = 'Customer'

    def __str__(self):
        return f"{self.user.username} ----- {self.user.user_type}"

