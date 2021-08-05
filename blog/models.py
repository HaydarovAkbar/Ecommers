from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    level = models.CharField(max_length=200, null=True)
    cafedra = models.CharField(max_length=200, null=True)
    faculty = models.CharField(max_length=200, null=True)
    row_date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(default="")

    @property
    def imageURL(self):
        try:
            return self.image.url
        except:
            return ""

    @property
    def full_name(self):
        return self.user.first_name + " " + self.user.last_name

    def __str__(self):
        return self.full_name


class Articel(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    name = models.CharField(max_length=400)
    text = models.TextField()
    tags = models.CharField(max_length=300, null=True)
    published_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class LinkedFiles(models.Model):
    articel = models.ForeignKey(Articel, on_delete=models.CASCADE)
    files = models.FileField()
    description = models.CharField(max_length=400, null=True)

    @property
    def file_URL(self):
        try:
            return self.files.url
        except:
            return ""
