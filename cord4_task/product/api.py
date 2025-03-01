from rest_framework import viewsets, permissions
from rest_framework.permissions import IsAdminUser

from cord4_task.product.models import Product
from cord4_task.product.serializers import ProductSerializer
from cord4_task.utils.permission import IsReadAction


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.filter(is_deleted=False)
    serializer_class = ProductSerializer
    permission_classes = (permissions.IsAuthenticated, IsReadAction | IsAdminUser,)
    ordering_fields = ('created',)


