from rest_framework.routers import DefaultRouter

from products.views import ProductsView

router = DefaultRouter()

router.register(r'products', ProductsView, basename='products')

urlpatterns = router.urls
