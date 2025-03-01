from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator
from cord4_task.custom_auth.managers import ApplicationUserManager
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.
class BaseModel(models.Model):
    is_active = models.BooleanField(default=True)
    is_delete = models.BooleanField(default=False)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class ApplicationUser(AbstractBaseUser, BaseModel, PermissionsMixin):
    username_validator = UnicodeUsernameValidator()
    email = models.EmailField('email address', unique=True, null=True, blank=True,
                              error_messages={'unique': 'A user with that email already exists.'},)
    username = models.CharField('username', max_length=150, unique=True, null=True, blank=True,
                                validators=[username_validator],)
    first_name = models.CharField('first name', max_length=30, blank=True)
    last_name = models.CharField('last name', max_length=150, blank=True)
    phone = PhoneNumberField('phone', null=True, blank=True, unique=True)
    is_active = models.BooleanField('active', default=True)
    is_staff = models.BooleanField('staff status', default=False)

    # USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['username']

    objects = ApplicationUserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return f'{self.email}'

    def save(self, *args, **kwargs):
        if self.email:
            self.email = self.__class__.objects.normalize_email(self.email)

        return super(ApplicationUser, self).save(*args, **kwargs)

