from rest_framework import serializers
from .models import Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'is_deleted']
        read_only_fields = ['id', 'is_deleted']


class FileUploadSerializer(serializers.Serializer):
    file = serializers.FileField()


