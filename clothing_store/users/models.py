from django.db import models
from django.contrib.auth.models import AbstractUser

from products.models import Product


class User(AbstractUser):
    """
    Модель пользователя
    """
    username = models.CharField(max_length=25, unique=True)
    name = models.CharField(max_length=120)
    surname = models.CharField(max_length=120)
    email = models.EmailField(unique=True, blank=True, null=True)
    phone = models.CharField(max_length=20, unique=True, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.username

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Favorite(models.Model):
    """
    Модель избранных товаров у пользователя
    """
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='favorites')
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.user} added {self.product} to favorites'

    class Meta:
        unique_together = ('user', 'product')
        ordering = ['-created_at']
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'
