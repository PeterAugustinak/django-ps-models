from django.db import models


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

    def __str__(self):
        return f"product: {self.name}: {self.price} EUR, left: " \
               f"{self.stock_count}"


class ProductImage(models.Model):
    image = models.ImageField()
    # quotes in 'Product' serves in case that Product class is not defined yet
    product = models.ForeignKey('Product', on_delete=models.CASCADE)

    def __str__(self):
        return f"The image for product {self.product.name}"


class Category(models.Model):
    name = models.CharField(max_length=30)
    product = models.ManyToManyField('Product')

    def __str__(self):
        return f"Category {self.name}"
