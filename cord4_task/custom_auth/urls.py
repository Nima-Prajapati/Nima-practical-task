from django.urls import path, include
from rest_framework.routers import SimpleRouter
from . import views
from .api import RegistrationViewSet, UserAuthViewSet, UserViewSet

router = SimpleRouter()
router.register('', UserAuthViewSet, basename='auth')
router.register('register', RegistrationViewSet, basename='registration')
router.register('users', UserViewSet, basename='users')

app_name = 'custom_auth'

urlpatterns = [
    path('', include(router.urls)),
]

