from rest_framework import viewsets, status
from rest_framework.permissions import (
    AllowAny, IsAuthenticated, IsAdminUser
)
from rest_framework.decorators import action
from rest_framework.response import Response

from django.db.models import Q

from products.models import Product
from products.serializers import ProductSerializer, ProductDetailSerializer

from users.models import Favorite


class ProductsView(viewsets.ModelViewSet):
    """
    Класс предсттавляет список товаров, при детальном и при полном отображении
    применяются разные сериалайзеры, так же при разных методах применяется 
    разные уровни доступа.
    """
    queryset = Product.objects.filter(is_active=True)

    def get_serializer_class(self):
        if self.action == 'list':
            return ProductSerializer
        return ProductDetailSerializer

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy', 'create']:
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        queryset = self.queryset

        size_ids = self.request.query_params.getlist('size')
        color_ids = self.request.query_params.getlist('color')
        brand_ids = self.request.query_params.getlist('brand')
        category_ids = self.request.query_params.getlist('category')
        search_query = self.request.query_params.get('search')

        if size_ids:
            size_filter = Q(dimensions__id__in=size_ids)
            queryset = queryset.filter(size_filter)

        if color_ids:
            color_filter = Q(colors__id__in=color_ids)
            queryset = queryset.filter(color_filter)

        if brand_ids:
            brand_filter = Q(brand__id__in=brand_ids)
            queryset = queryset.filter(brand_filter)

        if category_ids:
            category_filter = Q(category__id__in=category_ids)
            queryset = queryset.filter(category_filter)

        if search_query:
            search_filter = Q(name__icontains=search_query) | Q(
                description__icontains=search_query)
            queryset = queryset.filter(search_filter)

        return queryset
