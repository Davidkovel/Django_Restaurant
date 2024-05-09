from django.urls import path
from . import views
# from .views import PaymentView

urlpatterns = [
    path('cart/', views.cart_view, name='cart'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('clear_cart/', views.clear_cart, name='clear_cart'),
    path('remove_from_cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
   # path('payment/', PaymentView.as_view(), name='payment'),
]

