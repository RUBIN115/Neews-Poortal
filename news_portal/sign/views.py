from django.contrib.auth.models import User
from django.views.generic.edit import CreateView
from .models import BaseRegisterForm
from django.shortcuts import render, reverse, redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from news.models import Post


class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = '/news/'


@login_required
def upgrade_me(request):
    user = request.user
    authors_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        authors_group.user_set.add(user)
    return redirect('/news')


# class CategoryListView(ListView):
#     model = Post
#     template_name = 'category_list.html'
#     context_object_name = 'category_news_list'
#
#     def get_queryset(self):
#         self.category = get_object_or_404(Category, id=self.kwargs['pk'])
#         queryset = Post.objects.filter(category=self.category).order_by('-time_in')
#         return queryset
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['is_not_subscriber'] = self.request.user not in self.category.subscribers.all()
#         context['category'] = self.category
#         return context


# @login_required
# def subscribe(request, pk):
#     user = request.user
#     category = Category.objects.get(id=pk)
#     category.subscribers.add(user)
#
#     html_content = render_to_string(
#         'send_email.html',
#         {
#             'category': category.tematic,
#         }
#     )
#
#     msg = EmailMultiAlternatives(
#         subject=f'{user} {category.tematic}',
#         body=category.tematic,
#         from_email='ilhaosinkin@yandex.ru',
#         to=['ilaosinkin@gmail.com'],
#     )
#     msg.attach_alternative(html_content, "text/html")
#
#     msg.send()
#
#     message = 'Вы подписались на рассылку новостей категории'
#     return render(request, 'subscribe.html', {'category': category, 'message': message})
