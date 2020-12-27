from rest_framework import serializers
from .models import Profile, Category, List


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'


class ListSerializer(serializers.ModelSerializer):

    class Meta:
        model = List
        fields = '__all__'


