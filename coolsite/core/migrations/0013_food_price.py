# Generated by Django 4.2.3 on 2023-08-22 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_remove_cartitem_cart_remove_cartitem_food_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='food',
            name='price',
            field=models.IntegerField(null=True, verbose_name='Цена'),
        ),
    ]
