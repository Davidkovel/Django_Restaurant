# Generated by Django 4.2.3 on 2023-08-22 14:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_cart_cartitem_cart_items_cart_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartitem',
            name='cart',
        ),
        migrations.RemoveField(
            model_name='cartitem',
            name='food',
        ),
        migrations.DeleteModel(
            name='Cart',
        ),
        migrations.DeleteModel(
            name='CartItem',
        ),
    ]
