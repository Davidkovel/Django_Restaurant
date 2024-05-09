from django.urls import path, re_path
from django.views.decorators.cache import cache_page
from .views import *

urlpatterns = [
    path('', MainPage.as_view(), name='home'),
    path('post/<slug:post_slug>/', cache_page(60)(ShowPost.as_view()), name='post'),
    path('category/<int:cat_id>/', ShowCategory.as_view(), name='category'),
    path('book_table/', BookTableList.as_view(), name='book_table'),
#    path('book_table/<int:pk>/', BookTableUpdate.as_view(), name="booktable_update"),
    path('about/', About.as_view(), name='about'),
    path('contact/', Contact.as_view(), name='contact'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('forward/', SendText.as_view(), name='send_text'),
    path('post/<slug:post_slug>/comment_create/', ShowPost.as_view(), name='comment_create'),
    path('post/<int:pk>/reply_create/', ReplyCreateView.as_view(), name='reply_create'),
]