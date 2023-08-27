from django.contrib import admin
from .models import *


class FoodAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "time_upload", "category_id")
    list_display_links = ("id", "title")
    list_filter = ("title", "id", "time_create")
    search_fields = ("title", "content")


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    list_display_links = ("id", "name")
    search_fields = ("name",)


admin.site.register(Food, FoodAdmin)
admin.site.register(Category, CategoryAdmin)
