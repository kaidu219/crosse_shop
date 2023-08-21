from rest_framework import serializers
from rest_framework.response import Response

from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from django.db.utils import IntegrityError

from users.models import User, Favorite

from products.serializers import ProductSerializer
from products.models import Product

import re


class UserSerializer(serializers.ModelSerializer):
    """
    Сериалайзер для отображения информации о пользователе
    """
    favorite_products = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'phone',
                  'password', 'name', 'surname', 'favorite_products')
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True},
            'phone': {'required': True}
        }

    def get_favorite_products(self, user):
        return user.favorites.values_list('product_id', flat=True)

    def validate_phone(self, value):
        """
        Функция для проверки правильности заполнения телефон номера
        """
        phone_regex = r'^[\d\+\-\(\) ]+$'
        if not re.match(phone_regex, value):
            raise serializers.ValidationError(
                "Неверный формат номера телефона")
        return value

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    """
    Сериалайзер для аутентификации пользователя, 
    в котором нужно отправлять username и password
    """
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)

    def validate(self, data):
        username = data.get('username', None)
        password = data.get('password', None)
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise serializers.ValidationError('Неверные учетные данные')
        else:
            raise serializers.ValidationError(
                'Необходимо ввести username и password')
        return data


class FavoriteSerializer(serializers.ModelSerializer):
    """
    Сериалайзер для отображения избранных товаров пользователя
    при создании, нужно отправлять id товара,
    также он проверят чтобы один и тот же товар не добавлялся снова 
    """
    product_id = serializers.IntegerField()

    class Meta:
        model = Favorite
        fields = ('id', 'product_id')

    def to_representation(self, instance):
        context = super().to_representation(instance)
        context['product'] = ProductSerializer(instance.product).data
        return context

    def create(self, validated_data):
        product_id = self.initial_data.get('product_id')
        user = self.context['user']
        try:
            product = get_object_or_404(Product, id=product_id)
            return Favorite.objects.create(user=user, product=product)
        except IntegrityError:
            raise serializers.ValidationError(
                'Этот товар уже добавлен в избранное')
