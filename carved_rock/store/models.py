from decimal import Decimal

from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class ProductInStockQuerySet(models.QuerySet):
    def in_stock(self):
        return self.filter(stock_count__gt=0)

class Product(models.Model):
    name = models.CharField(max_length=100)
    stock_count = models.IntegerField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.TextField(default="", blank=True)
    sku = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="stock keeping unit",
        help_text="Please add unique value",
        default="a"
    )
    slug = models.SlugField()
    # now Product can be used with .objects and with .stock (where only product
    # that are in stock will be
    objects = ProductInStockQuerySet.as_manager()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


    class Meta:
        db_table = 'product'
        ordering = ['price', 'name']
        # constraints = [
        #     models.CheckConstraint(check=models.Q(price__gte=0),
        #                            name='price_not_negative_check')
        #                ]

    @property
    def vat(self):
        return Decimal(.2) * self.price

    def get_absolute_url(self):
        return reverse("store:product-detail", kwargs={'pk': self.id})

    def __str__(self):
        return f"product: {self.name}: {self.price} EUR, left: " \
               f"{self.stock_count}"


class OrderedProducts(Product):
    class Meta:
        proxy = True
        ordering = ['name']


class ProductImage(models.Model):
    image = models.ImageField()
    # quotes in 'Product' serves in case that Product class is not defined yet
    product = models.ForeignKey(
        'Product', on_delete=models.CASCADE, related_name="images"
    )

    class Meta:
        db_table = 'product_image'

    def __str__(self):
        return f"The image for product {self.product.name}"


class Category(models.Model):
    name = models.CharField(max_length=30)
    products = models.ManyToManyField('Product', related_name="categories")

    class Meta:
        db_table = 'category'
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return f"Category {self.name}"
