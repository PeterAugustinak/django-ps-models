from django.shortcuts import render

from .models import Product
# Create your views here.

def category_view(request, name):
    products = Product.objects.filter(categories__name=name)

    return render(
        request,
        "store/category.html",
        {
            "products": products,
            "category_name": name,
            }
        )
