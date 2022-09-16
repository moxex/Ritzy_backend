from django.db import models
from django.contrib.auth import get_user_model

from apps.common.models import TimeStampedUUIDModel

User = get_user_model()

CATEGORY_CHOICES = (
    ('SB', 'Shirts And Blouses'),
    ('AN', 'Ankara Materials'),
    ('SK', 'Skirts'),
    ('MT', 'Materials')
)

LABEL_CHOICES = (
    ('Sale', 'sale'),
    ('New', 'new'),
    ('Promotion', 'promotion')
)


class Category(TimeStampedUUIDModel):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=200, unique=True)
    cat_choices = models.CharField(choices=CATEGORY_CHOICES, max_length=50)
    description = models.TextField()

    class Meta:
        ordering = ('name', )
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


class Product(TimeStampedUUIDModel):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True)
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
    description = models.TextField(blank=True)
    label = models.CharField(choices=LABEL_CHOICES, max_length=10)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)

    class Meta:
        ordering = ('name',)
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.name


class Order(models.Model):
    PAYMENT_STATUS_PENDING = 'P'
    PAYMENT_STATUS_COMPLETE = 'C'
    PAYMENT_STATUS_FAILED = 'F'
    PAYMENT_STATUS_CHOICES = [
        (PAYMENT_STATUS_PENDING, 'Pending'),
        (PAYMENT_STATUS_COMPLETE, 'Complete'),
        (PAYMENT_STATUS_FAILED, 'Failed')
    ]

    placed_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(
        max_length=1, choices=PAYMENT_STATUS_CHOICES, default=PAYMENT_STATUS_PENDING)
    customer = models.ForeignKey(User, on_delete=models.PROTECT)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)


class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    customer = models.ForeignKey(
        User, on_delete=models.CASCADE)