from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework.settings import api_settings
from phonenumber_field.serializerfields import PhoneNumberField
# from django.utils.translation import gettext as _

User = get_user_model()


class RegistrationSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        extra_kwargs = {
            'password': {'write_only': True, 'validators': [validate_password]},
            'email': {'required': True},
        }
        # read_only_fields = ('email',)

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = super().create(validated_data)

        # password assignment
        user.set_password(password)
        user.save(update_fields=['password'])

        return user


class LoginSerializer(serializers.Serializer):
    fail_login_message = ''

    def authenticate(self):
        user = authenticate(**self.validated_data)
        if not user:
            raise serializers.ValidationError({
                # api_settings.NON_FIELD_ERRORS_KEY: [_(self.fail_login_message)],
                api_settings.NON_FIELD_ERRORS_KEY: [self.fail_login_message],
            })

        return user


class UserAuthSerializer(LoginSerializer):
    email = serializers.CharField(required=True)
    password = serializers.CharField()
    fail_login_message = 'Invalid credentials.'


class UserSelfSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'email', )
        read_only_fields = ('id',)


class CheckEmailData(serializers.Serializer):
    email = serializers.EmailField(required=True)