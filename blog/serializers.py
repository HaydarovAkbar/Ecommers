from rest_framework import serializers
from .models import *


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = "__all__"


class ArticelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Articel
        fields = "__all__"


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = LinkedFiles
        fields = "__all__"

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

class TopshiriqSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = "__all__"