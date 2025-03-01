from datetime import datetime

from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.utils.translation import gettext as _

from rest_framework.exceptions import PermissionDenied
from django.contrib.auth import get_user_model

from django.contrib.auth.backends import BaseBackend

User = get_user_model()


class CustomModelBackend(ModelBackend):
    """
    Authenticate user using email
    """

    def authenticate(self, request, username=None, email=None, password=None, **kwargs):
        if not username and not email:
            return None

        user_model = get_user_model()

        username_query_dict = {'username__iexact': username}
        email_query_dict = {'email__iexact': email}

        try:
            query_filter = Q()
            if username:
                query_filter |= Q(**username_query_dict)
            if email:
                query_filter |= Q(**email_query_dict)

            user = user_model.objects.get(query_filter)

            if not user.is_active:
                raise PermissionDenied(_('User is not active.'))

        except user_model.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user

        return None



