# Generated by Django 4.1.1 on 2022-09-09 07:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_category'),
    ]

    operations = [
        migrations.RenameField(
            model_name='category',
            old_name='product',
            new_name='products',
        ),
    ]
