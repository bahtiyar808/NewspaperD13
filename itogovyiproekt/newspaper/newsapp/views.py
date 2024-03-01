from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Exists, OuterRef
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_protect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Category, Subscriber
import datetime
from .filters import PostFilter
from .forms import PostForm
from django.core.cache import cache
import logging



class NewsList(ListView):
    model = Post
    ordering = '-date_time'
    template_name = 'all_news.html'
    context_object_name = 'posts'
    paginate_by = 10


    def get_queryset(self):

        return Post.objects.filter(choice='N').order_by('-date_time')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['time_now'] = datetime.datetime.utcnow()
        context['next_sale'] = None
        return context



class ArticleList(ListView):
    model = Post
    ordering = '-date_time'
    template_name = 'all_articles.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        return Post.objects.filter(choice='A').order_by('-date_time')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['time_now'] = datetime.datetime.utcnow()
        context['next_sale'] = None
        return context


class NewsDetail(DetailView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'posts'
    queryset = Post.objects.all()

    def get_object(self, *args, **kwargs):
        obj = cache.get(f'news-{self.kwargs["pk"]}', None)
        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'news-{self.kwargs["pk"]}', obj)
        return obj


class NewsSearch(ListView):
    model = Post
    ordering = '-date_time'
    template_name = 'news_search.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class NewsCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('newsapp.add_post')
    form_class = PostForm
    model = Post
    template_name = 'news_create.html'

    def form_valid(self, form):
        post = form.save(commit= False)
        post.choice = 'N'

        return super().form_valid(form)



class ArticleCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('newsapp.add_post')
    form_class = PostForm
    model = Post
    template_name = 'article_create.html'

    def form_valid(self, form):
        post = form.save(commit= False)
        post.choice = 'A'
        return super().form_valid(form)

class NewsEdit(PermissionRequiredMixin, UpdateView):
    permission_required = ('newsapp.change_post')
    form_class = PostForm
    model = Post
    template_name = 'news_create.html'

    def form_valid(self, form):
        post = form.save(commit= False)
        post.choice = 'N'
        return super().form_valid(form)


class ArticleEdit(PermissionRequiredMixin, UpdateView):
    permission_required = ('newsapp.change_post')
    form_class = PostForm
    model = Post
    template_name = 'article_create.html'

    def from_valid(self, form):
        post = form.save(commit=False)
        post.choice = 'N'
        return super().form_valid(form)


class NewsDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('newsapp.delete_post')
    model = Post
    template_name = 'news_delete.html'
    success_url = reverse_lazy('news_list')

    def from_valid(self, form):
        post = form.save(commit=False)
        post.choice = 'N'
        return super().form_valid(form)


class ArticleDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('newsapp.delete_post')
    model = Post
    template_name = 'articles_delete.html'
    success_url = reverse_lazy('article_list')

    def from_valid(self, form):
        post = form.save(commit=False)
        post.choice = 'A'
        return super().form_valid(form)

@login_required
@csrf_protect
def subscriptions(request):
    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        category = Category.objects.get(id=category_id)
        action = request.POST.get('action')

        if action == 'subscribe':
            Subscriber.objects.create(user=request.user, category=category)
        elif action == 'unsubscribe':
            Subscriber.objects.filter(
                user=request.user,
                category=category,
            ).delete()

    categories_with_subscriptions = Category.objects.annotate(
        user_subscribed=Exists(
            Subscriber.objects.filter(
                user=request.user,
                category=OuterRef('pk'),
            )
        )
    ).order_by('category_name')
    return render(
        request,
        'subscriptions.html',
        {'categories': categories_with_subscriptions},
    )


