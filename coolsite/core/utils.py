from django.core.cache import cache

from .models import *
menu = [{"title": "О нас", "url_name": "about"},
        {"title": "Заказать стол", "url_name": "book_table"},
        {"title": "Обратная связь", "url_name": "contact"},
        {"title": "Корзина", "url_name": "cart"},
        {"title": "Чат", "url_name": "chat"},
        {"title": "Отправка текст", "url_name": "send_text"},
        ]


class UpdateTableMixin:
    def update_table(self, table_id, user):
        try:
            table = BookTable.objects.get(pk=table_id)
            table.user_book = user
            table.is_busy = True
            table.save()
        except Exception as ex:
            print('Error!!', ex)


class DataMixin:
    def get_user_context(self, **kwargs):
        context = kwargs

        cats = cache.get("cats")
        if not cats:
            cats = Category.objects.all()
            cache.set("cats", cats, 15)

        user_menu = menu.copy()
        if not self.request.user.is_authenticated:
            user_menu.pop(1)

        context['menu'] = user_menu
        context['cats'] = cats

        if 'cat_selected' not in context:
            context['cat_selected'] = 0
        return context
