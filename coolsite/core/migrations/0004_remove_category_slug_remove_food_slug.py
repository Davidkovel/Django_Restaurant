# Generated by Django 4.2.3 on 2023-08-03 18:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_alter_category_options_alter_food_options_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='slug',
        ),
        migrations.RemoveField(
            model_name='food',
            name='slug',
        ),
    ]
