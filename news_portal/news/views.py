from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView)
from .models import Post, Category
from .filters import NewsFilter
from .forms import NewForm

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin

from django.http import HttpResponseRedirect

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render

class NewsList(ListView):
    # model = Post
    queryset = Post.objects.filter(type=0)
    ordering = '-date_time_create'
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 10

class NewDetail(DetailView):
    model = Post
    template_name = 'new.html'
    context_object_name = 'new'
    form_class = NewForm


class SearchNewsList(ListView):
    queryset = Post.objects.filter(type=0)
    ordering = '-date_time_create'
    template_name = 'search.html'
    context_object_name = 'news'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = NewsFilter(self.request.GET, queryset=self.get_queryset())
        return context

class AddNew(CreateView):
    template_name = 'new_add.html'
    form_class = NewForm

    def form_valid(self, form):
        post = form.save(commit=False)
        post.post_type = 0
        return super().form_valid(form)


class UpdateNew(UpdateView):
    template_name = 'new_update.html'
    form_class = NewForm

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)
class DeleteNew(DeleteView):
    template_name = 'new_delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'
    context_object_name = 'new'

class CategoryList(ListView):
    model = Category
    queryset = Category.objects.all()
    template_name = 'categories.html'
    context_object_name = 'categories'

class CategoryDetail(DetailView):
    model = Category
    template_name = 'one_category.html'
    context_object_name = 'one_category'

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(category=self.category).order_by('-date_time_create')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = Category.objects.get(pk=self.kwargs['pk'])
        context['cat'] = category
        context['subscribers'] = category.subscribers.all()
        return context

def subscribe(request, pk):
    category = Category.objects.get(pk=pk)
    category.subscribers.add(request.user.id)
    return HttpResponseRedirect(reverse('categories'))


def unsubscribe(request, pk):
    category = Category.objects.get(pk=pk)
    category.subscribers.remove(request.user.id)
    return HttpResponseRedirect(reverse('categories'))