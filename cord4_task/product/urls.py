from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .api import ProductViewSet

router = SimpleRouter()
router.register('', ProductViewSet, basename='category')

app_name = 'product'

urlpatterns = [
    path('', include(router.urls)),
]

