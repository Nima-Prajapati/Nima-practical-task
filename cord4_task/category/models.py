from django.db import models
from django.utils.text import slugify
from model_utils.models import TimeStampedModel


class Category(TimeStampedModel):
    name = models.CharField(
        'name',
        max_length=150,
        unique=True,
        error_messages={'unique': 'A category with that name already exists'}
    )
    description = models.TextField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return f'{self.name}'


class SubCategory(TimeStampedModel):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name = 'Category')
    name = models.CharField(
        'name',
        max_length=150,
        help_text="The sub category name."
    )
    description = models.TextField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Sub-Category'
        verbose_name_plural = 'Sub-Categories'

    def __str__(self):
        return f'{self.name}'

