# Generated by Django 4.2.3 on 2023-07-31 21:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_alter_product_is_active'),
        ('users', '0002_favorite_delete_selectedproducts'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='favorite',
            unique_together={('user', 'product')},
        ),
    ]
