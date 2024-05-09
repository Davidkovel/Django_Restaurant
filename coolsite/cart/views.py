from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
# import stripe
from django.views import View

from core.models import Food, Category
from .cart import Cart

menu = [{"title": "О нас", "url_name": "about"},
        {"title": "Заказать стол", "url_name": "book_table"},
        {"title": "Обратная связь", "url_name": "contact"},
        {"title": "Корзина", "url_name": "cart"},
        {"title": "Чат", "url_name": "chat"},
        ]

# stripe.api_key = settings.STRIPE_SECRET_KEY

def cart_view(request):
    cart = Cart(request)
    cats = Category.objects.all()

    context = {'cart': cart}
    context['cats'] = cats

    user_menu = menu.copy()

    if not request.user.is_authenticated:
        user_menu.pop(1)

    context['menu'] = user_menu

    if 'cat_selected' not in context:
        context['cat_selected'] = 0

    return render(request, 'cart/cart.html', context)


def add_to_cart(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Food, id=product_id)
    cart.add(product)
    return redirect('cart')


def clear_cart(request):
    cart = Cart(request)
    cart.clear()
    return redirect('cart')


def remove_from_cart(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Food, id=product_id)
    cart.remove(product)
    return redirect('home')

# payment --

# class PaymentView(View):
#     def get(self, request):
#         cart = Cart(request)
#         total_price = cart.get_total_price()
#         publishable_key = settings.STRIPE_PUBLISHABLE_KEY
#         return render(request, 'cart/payment.html', {'total_price': total_price, 'publishable_key': publishable_key})
#
#     def post(self, request):
#         cart = Cart(request)
#         total_price = cart.get_total_price()
#
#         try:
#             # payment_intent = stripe.PaymentIntent.create(
#             #     amount=int(total_price * 100),
#             #     currency='usd',
#             # )
#
#             return render(request, 'cart/payment.html', {
#                 'client_secret': payment_intent.client_secret,
#                 'total_price': total_price,
#                 'publishable_key': settings.STRIPE_PUBLISHABLE_KEY,
#             })
#
#         except Exception as ex:
#             return redirect('cart')