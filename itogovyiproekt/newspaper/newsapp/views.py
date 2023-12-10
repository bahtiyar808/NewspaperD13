from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post
import datetime
from .filters import PostFilter
from .forms import PostForm

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


class NewsCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'news_create.html'

    def form_valid(self, form):
        post = form.save(commit= False)
        post.choice = 'N'
        return super().form_valid(form)


class ArticleCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'article_create.html'

    def form_valid(self, form):
        post = form.save(commit= False)
        post.choice = 'A'
        return super().form_valid(form)

class NewsEdit(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'news_create.html'

    def form_valid(self, form):
        post = form.save(commit= False)
        post.choice = 'N'
        return super().form_valid(form)


class ArticleEdit(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'article_create.html'

    def from_valid(self, form):
        post = form.save(commit=False)
        post.choice = 'N'
        return super().form_valid(form)


class NewsDelete(DeleteView):
    model = Post
    template_name = 'news_delete.html'
    success_url = reverse_lazy('news_list')

    def from_valid(self, form):
        post = form.save(commit=False)
        post.choice = 'N'
        return super().form_valid(form)


class ArticleDelete(DeleteView):
    model = Post
    template_name = 'articles_delete.html'
    success_url = reverse_lazy('article_list')

    def from_valid(self, form):
        post = form.save(commit=False)
        post.choice = 'A'
        return super().form_valid(form)