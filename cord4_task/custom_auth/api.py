from django.conf import settings
from rest_framework import status, viewsets, permissions
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from django.contrib.auth import get_user_model
from templated_email import send_templated_mail
from cord4_task.custom_auth.serializers import RegistrationSerializer, UserAuthSerializer, UserSelfSerializer, \
    CheckEmailData
from cord4_task.utils.permission import IsReadAction, IsSelf

User = get_user_model()


class RegistrationViewSet(
    CreateModelMixin,
    GenericViewSet,
):
    queryset = User.objects.all()
    serializer_class = RegistrationSerializer
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        """user registration """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        serializer = UserSelfSerializer(instance=user, context={'request': request, 'view': self}).data
        serializer.update(UserAuthViewSet.get_success_headers(user=user))
        return Response(status=status.HTTP_201_CREATED, data=serializer)


class UserAuthViewSet(viewsets.ViewSet):
    NEW_TOKEN_HEADER = 'X-Token'
    login_serializer_class = UserAuthSerializer
    serializer_class = UserSelfSerializer

    @action(detail=False, methods=['post'], permission_classes=[permissions.AllowAny], url_path='login')
    def basic_login(self, request):
        """ Login user using email """
        serializer = self.get_login_serializer()
        serializer.is_valid(raise_exception=True)
        user = serializer.authenticate()
        serializer = self.serializer_class(instance=user, context={'request': request, 'view': self}).data
        user.user_auth_tokens.all().delete()
        serializer.update(self.get_success_headers(user))
        return Response(status=status.HTTP_201_CREATED, data=serializer)

    def get_login_serializer(self, **kwargs):
        return self.login_serializer_class(data=self.request.data, **kwargs)

    @classmethod
    def get_success_headers(cls, user):
        return {cls.NEW_TOKEN_HEADER: user.user_auth_tokens.create().key}

    @action(methods=['delete'], detail=False,
            permission_classes=[permissions.AllowAny, permissions.IsAuthenticated])
    def logout(self, request, *args, **kwargs):
        request.user.user_auth_tokens.all().delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class UserViewSet(
    RetrieveModelMixin,
    UpdateModelMixin,
    GenericViewSet
):
    queryset = User.objects.filter(is_superuser=False, is_active=True, is_delete=False)
    permission_classes = [permissions.IsAuthenticated, IsReadAction | IsSelf]
    serializer_class = UserSelfSerializer

    @action(methods=['post'], detail=False, permission_classes=[permissions.AllowAny],
            url_path='reset-password-email', url_name='reset_password_email', serializer_class=CheckEmailData)
    def reset_password_email(self, request, *args, **kwargs):
        """
        Sending Reset password mail.
        """
        serializer = self.get_serializer(data=self.request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(email__iexact=serializer.validated_data.get('email')).first()
        if not user:
            raise NotFound("User doesn't exists.")

        send_templated_mail(
            template_name="auth/user_password_reset",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            context={
                'subject_name': "Reset Password",
            }
        )

        return Response({"message": "Email has been sent."})

