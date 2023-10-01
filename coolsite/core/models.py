from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

class Food(models.Model):
    title = models.CharField(max_length=255, verbose_name="Названия")
    content = models.TextField(blank=True, verbose_name="Описания")
    price = models.IntegerField(null=True, verbose_name="Цена")
    slug = models.SlugField(max_length=255, unique=True, null=True, db_index=True, verbose_name="URL")
    photo = models.ImageField(upload_to='photos/%Y/%m/%d', verbose_name="Фото")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создание")
    time_upload = models.DateTimeField(auto_now=True, verbose_name="Время изменения")
    category = models.ForeignKey('Category', on_delete=models.PROTECT, null=True, verbose_name="Категория")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})

    class Meta:
        verbose_name = "Меню"
        verbose_name_plural = 'Меню'
        ordering = ['title']


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name="Категория")
    slug = models.SlugField(max_length=255, unique=True, null=True, db_index=True, verbose_name="URL")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_id': self.pk})

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = 'Категория'
        ordering = ['name']


class BookTable(models.Model):
    table = models.CharField(max_length=100, db_index=True, null=True, verbose_name="Стол")
    user_book = models.ForeignKey(User, null=True, verbose_name='Клиент', on_delete=models.CASCADE)
    is_busy = models.BooleanField(default=True, verbose_name="Занятый стол")

    def __str__(self):
        return self.table

    class Meta:
        verbose_name = "Зарезервировать стол"
        verbose_name_plural = "Зарезервировать столы"
        ordering = ['table']


class Contact(models.Model):
    name = models.CharField(max_length=100, verbose_name="Имя")
    email = models.CharField(max_length=50, null=True)
    content = models.TextField(blank=True, verbose_name="Описания")

    class Meta:
        verbose_name = "Отзивы"
        verbose_name_plural = "Отзивы"
        ordering = ["id"]
