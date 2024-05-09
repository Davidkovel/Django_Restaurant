from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, TemplateView, UpdateView, FormView

from .forms import *
from .utils import *
from .models import *
# from .service import send
# from .tasks import send_spam_email, send_user_text


class MainPage(DataMixin, ListView):
    model = Food
    template_name = 'core/index.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Главная Страница')
        return context | c_def

    def get_queryset(self):
        return Food.objects.filter().select_related('category')


class ShowPost(DataMixin, DetailView):
    model = Food
    template_name = 'core/post.html'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="")
        context['comments'] = self.object.comments.all()
        context['form'] = CommentForm()
        return context | c_def

    def get_object(self, queryset=None):
        post_slug = self.kwargs['post_slug']
        return Food.objects.get(slug=post_slug)

    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.food = self.get_object()
            comment.save()
            return redirect('post', post_slug=self.get_object().slug)

        context = self.get_context_data()
        context['form'] = form
        return self.render_to_response(context)


class ReplyCreateView(View):
    template_name = 'core/post.html'

    def post(self, request, pk, *args, **kwargs):
        comment = get_object_or_404(Comment, pk=pk)
        form = ReplyForm(request.POST)

        if form.is_valid():
            reply = form.save(commit=False)
            reply.user = request.user
            reply.comment = comment
            reply.save()
            return redirect('post', post_slug=comment.food.slug)

        show_post_view = ShowPost()
        context = show_post_view.get_context_data(post=comment.food)
        context['form'] = form
        return render(request, self.template_name, context)


# def comment_create(request):
#     if request.method == "POST":
#         form = CommentForm(request.POST)
#         if form.is_valid():
#             comment = form.save(commit=False)
#             comment.user = request.user
#             comment.save()
#             return redirect('comment_create', pk=comment.pk)
#     else:
#         form = CommentForm()
#     return render(request, 'core/post.html', {'form': form})


# def reply_create(request, pk):
#     comment = get_object_or_404(Comment, pk=pk)
#     if request.method == "POST":
#         form = ReplyForm(request.POST)
#         if form.is_valid():
#             reply = form.save(commit=False)
#             reply.user = request.user
#             reply.comment = comment
#             reply.save()
#             return redirect('reply_detail', pk=reply.pk)
#     else:
#         form = ReplyForm()
#     return render(request, 'core/post.html', {'form': form})


class ShowCategory(DataMixin, ListView):  # ListView - отображения списка объектов модели в шаблоне.
    model = Food
    template_name = 'core/index.html'
    context_object_name = 'posts'

    def get_queryset(self):
        cat_id = self.kwargs.get('cat_id')
        return Food.objects.filter(category_id=cat_id)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c = Category.objects.get(pk=self.kwargs['cat_id'])
        c_def = self.get_user_context(title='Категория -' + str(c.name),
                                      cat_selected=c.pk)
        return context | c_def


class About(DataMixin, TemplateView):  # TemplateView - позволяет отображать шаблон без использования модели
    template_name = 'core/about.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Страница о нас')
        return context | c_def


class Contact(DataMixin, CreateView):
    model = Contact
    form_class = ContactForm
    template_name = 'core/contact.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Обратная связь")
        return context | c_def

    def form_valid(self, form):
        form.save()
        #        send(form.istance.email)
        # send_spam_email.delay(form.instance.email)
        return super().form_valid(form)


class BookTableList(LoginRequiredMixin, DataMixin, UpdateTableMixin, CreateView):
    model = BookTable
    form_class = BookTableForm
    template_name = 'core/book_table.html'
    context_object_name = 'table_status'
    success_url = reverse_lazy('home')

    def get_queryset(self):
        return BookTable.objects.all()

    def user_has_reservation(self):
        return BookTable.objects.filter(user_book=self.request.user).exists()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Забронирувать стол")
        context['table_status'] = self.get_queryset()
        context['user'] = self.request.user
        context['user_has_reservation'] = self.user_has_reservation()

        return context | c_def

    def form_valid(self, form):
        table_id = self.request.POST.get('table')
        is_busy = self.request.POST.get('is_busy')

        if table_id and is_busy:
            self.update_table(table_id, self.request.user)

        else:
            print('Error: Missing table_id or user_book')
        # form.save()
        return redirect('home')


class SendText(DataMixin, CreateView):  # [TEST] for celery
    model = Forward
    form_class = ForwardForm
    template_name = "core/forward_text.html"
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Отправка текст")
        return context | c_def

    def form_valid(self, form):
        user_text = form.cleaned_data['user_text']
        # send_user_text(user_text)

        return super().form_valid(form)


class RegisterUser(DataMixin,
                   CreateView):  # CreateView - отображает форму для создания объекта, повторно отображает форму с ошибками валидации и сохраняет объект в базе данных.
    form_class = RegisterUserForm
    template_name = 'core/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Регистрация")
        return context | c_def

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'core/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Авторизация")
        return context | c_def

    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return redirect('login')
