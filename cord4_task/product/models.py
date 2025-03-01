import uuid
from django.db import models
from model_utils.models import TimeStampedModel
from django.conf import settings
from cord4_task.category.models import Category


def get_product_photo_path(instance, filename):
    return '{}/{}/{}'.format(settings.PRODUCT_IMAGES_PATH, uuid.uuid4(), filename)


# Create your models here.
class Product(TimeStampedModel):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Category')
    name = models.CharField('Name', max_length=150)
    price = models.FloatField("Selling price", null=True, blank=True)
    description = models.TextField('Description')
    stock_quantity = models.PositiveSmallIntegerField("Quantity available", default=0, null=True, blank=True)
    image = models.ImageField(
        upload_to=get_product_photo_path,
        height_field='height',
        width_field='width',
        null=True,
        blank=True
    )
    width = models.PositiveSmallIntegerField(blank=True, null=True)
    height = models.PositiveSmallIntegerField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.name}'

    def save(self, *args, **kwargs):
        if self.image and (not self.width or not self.height):
            self.width = self.image.width
            self.height = self.image.height

        super().save(*args, **kwargs)

