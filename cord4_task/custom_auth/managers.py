from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _


# class ApplicationUserManager(BaseUserManager):
#     use_in_migrations = True
#
#     def create_user(self, email, username, password, **extra_fields):
#         if not email:
#             raise ValueError(_('Email must be set'))
#         if not username:
#             raise ValueError(_('username must be set'))
#
#         email = self.normalize_email(email)
#         user = self.model(email=email, username=username, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user
#
#     def create_superuser(self, email, username, password, **extra_fields):
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)
#
#         if extra_fields.get('is_staff') is not True:
#             raise ValueError(_('Superuser must have is_staff=True.'))
#         if extra_fields.get('is_superuser') is not True:
#             raise ValueError(_('Superuser must have is_superuser=True.'))
#
#         return self.create_user(email, username, password, **extra_fields)
#
#     @classmethod
#     def normalize_email(cls, email):
#         if not email:
#             return None
#         return super().normalize_email(email)

class ApplicationUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Create User with the given email and password.
        :param email: user email
        :param password: user password
        :param extra_fields: all other extra fields
        :return: user
        """
        if not email:
            raise ValueError(_('The given email must be set'))
        email = self.normalize_email(email)

        user = self.model(email=email, **extra_fields)
        user.username = email
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create SuperUser with the given email and password.
        :param email: superuser email
        :param password: superuser password
        :param extra_fields: all other fields
        :return: superuser
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self._create_user(email, password, **extra_fields)

    @classmethod
    def normalize_email(cls, email):
        if not email:
            # using None instead of empty string if there's no email to bypass unique=True constraint
            return None
        return super().normalize_email(email)

    def get_by_natural_key(self, value):
        return self.get(**{'{user_name_field}__iexact'.format(user_name_field=self.model.USERNAME_FIELD): value})
