from django.urls import path
# Импортируем созданное нами представление
from .views import NewsList, NewsDetail, NewsSearch, NewsCreate, ArticleList, ArticleCreate, NewsEdit, ArticleEdit, \
   NewsDelete, ArticleDelete, subscriptions


urlpatterns = [
    path('news/', NewsList.as_view(), name='news_list'),
    path('articles/', ArticleList.as_view(), name='article_list'),
    path('<int:pk>', NewsDetail.as_view(), name='news_detail'),
    path('news/search/', NewsSearch.as_view(), name='news_search'),
    path('news/create/', NewsCreate.as_view(), name='news_create'),
    path('articles/create', ArticleCreate.as_view(), name='article_create'),
    path('news/<int:pk>/edit', NewsEdit.as_view(), name='news_edit'),
    path('articles/<int:pk>/edit', ArticleEdit.as_view(), name='articles_edit'),
    path('news/<int:pk>/delete', NewsDelete.as_view(), name='news_delete'),
    path('articles/<int:pk>/delete', ArticleDelete.as_view(), name='article_delete'),
    # path('subscriptions/', subscriptions, name='subscriptions'),
]
