from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .api import CategoryViewSet, CategoryUploadView

router = SimpleRouter()
router.register('category', CategoryViewSet, basename='category')

app_name = 'category'

urlpatterns = [
    # path('', include(router.urls)),
    path('upload/', CategoryUploadView.as_view(), name='category-upload'),
]

