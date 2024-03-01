from django.contrib.auth.models import User


from django.db import models
from django.db.models import Sum
from django.urls import reverse

from django.core.cache import cache


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_rate = models.IntegerField(default=0)

    def update_rating(self):

        sum_rating = self.post_set.aggregate(post_rating=Sum('post_rate'))
        result_sum_rating = 0

        try:
            result_sum_rating += sum_rating.get('post_rating')
        except TypeError:
            result_sum_rating = 0

        sum_comment_rating = self.author.comment_set.aggregate(comment_rating=Sum('comment_rate'))
        result_sum_comment_rating = 0
        result_sum_comment_rating += sum_comment_rating.get('comment_rating')
        self.user_rate = result_sum_rating * 3 + result_sum_comment_rating
        self.save()

    def __str__(self):
        return self.user.username


class Category(models.Model):
    category_name = models.CharField(max_length=255, unique=True)
    subscribers = models.ManyToManyField(User, through='Subscriber', related_name='categories')

    def __str__(self):
        return self.category_name


class Post(models.Model):
    Article_or_News = [
        ('A', 'Статья'),
        ('N', 'Новость')
    ]
    heading = models.CharField(max_length=50)
    text = models.TextField()
    post_rate = models.IntegerField(default=0)
    date_time = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    choice = models.CharField(max_length=1, choices=Article_or_News, default='N')
    categories = models.ManyToManyField(Category, through='PostCategory')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        cache.delete(f'news-{self.pk}')

    def __str__(self):
        return f'{self.heading.title()}: {self.text[:20]}'

    def like(self):
        self.post_rate += 1
        self.save()

    def dislike(self):
        self.post_rate -= 1
        self.save()

    def preview(self):
        return self.text[:125] + "..."

    def get_absolute_url(self):
        return reverse('news_detail', args=[str(self.id)])



class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.TextField(blank=True)
    date_time = models.DateTimeField(auto_now_add=True)
    comment_rate = models.IntegerField(default=0)

    def like(self):
        self.comment_rate += 1
        self.save()

    def dislike(self):
        self.comment_rate -= 1
        self.save()


class Subscriber(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='subscriptions',
    )
    category = models.ForeignKey(
        to='Category',
        on_delete=models.CASCADE,
        related_name='subscriptions',
    )
