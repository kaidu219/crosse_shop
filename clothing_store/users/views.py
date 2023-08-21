from django.shortcuts import render
from django.contrib.auth import authenticate
from django.db.utils import IntegrityError

from rest_framework import viewsets, mixins, generics
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveUpdateDestroyAPIView

from users.serializers import (
    UserSerializer, LoginSerializer, FavoriteSerializer
)
from users.models import Favorite, User
from users.permissions import IsOwnerOrAdmin


class UserDetailView(RetrieveUpdateDestroyAPIView):
    """
    Класс для отображения и изменения информации о текущем пользователе
    """
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class RegisterViewSet(viewsets.ViewSet):
    """
    Класс для регистрации пользователя
    """
    serializer_class = UserSerializer

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)


class LoginViewSet(viewsets.ViewSet):
    """
    Класс для аутентификации пользователя,
    после успешной аутентификации генериуется токен
    """
    serializer_class = LoginSerializer

    def create(self, request):
        serializer = self.serializer_class(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        user = authenticate(
            username=serializer.validated_data['username'],
            password=serializer.validated_data['password']
        )

        if not user:
            return Response({'error': 'Invalid credentials'}, status=400)

        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})


class FavoriteViewSet(mixins.ListModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    """
    Класс для отображения избранных товаров, 
    пользователь может только добавлять, удалять и 
    детально просмотривать избранные товары
    """
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Favorite.objects.filter(user=user)

    def create(self, request):
        user = request.user
        serializer = FavoriteSerializer(
            data=request.data, context={'user': user})
        if serializer.is_valid():
            try:
                serializer.save()
            except IntegrityError:
                return Response({'error': 'Этот товар уже добавлен в избранное'})
