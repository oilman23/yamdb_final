from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Avg

from .validators import validate_score, validate_year

User = get_user_model()


class Genre(models.Model):
    name = models.CharField(
        'Жанр', help_text='Жанр (драма, ужастик etc)', max_length=128
    )
    slug = models.SlugField(
        'Слаг жанра',
        max_length=64,
        unique=True,
        help_text='Слаг для жанра (drama, horror etc)',
    )

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.slug


class Category(models.Model):
    name = models.CharField(
        'Категория', help_text='Категория (фильм, книга etc)', max_length=128
    )
    slug = models.SlugField(
        'Слаг категории',
        max_length=64,
        unique=True,
        help_text='Слаг для категории (movie, book etc)',
    )

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.slug


class Title(models.Model):
    name = models.CharField(
        max_length=512,
        help_text='Наименование произведения',
    )
    year = models.IntegerField(
        blank=True,
        null=True,
        validators=[validate_year],
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        blank=True,
        null=True,
        help_text='Выберите категорию (фильм, книга etc)',
    )
    genre = models.ManyToManyField(
        Genre,
        through='GenreTitles',
        verbose_name='Жанр',
        related_name='titles',
    )
    description = models.CharField(
        verbose_name='Описание', max_length=512, default='description'
    )

    @property
    def rating(self):
        return self.reviews.all().aggregate(Avg('score'))['score__avg']

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name[:30]


class GenreTitles(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        verbose_name='Произведение',
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор отзыва',
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    text = models.TextField(verbose_name='Отзыв', help_text='Текст отзыва')
    score = models.PositiveSmallIntegerField(
        verbose_name='Рейтинг',
        help_text='Рейтинг произведения от 1 до 10',
        validators=[validate_score],
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации отзыва', auto_now_add=True
    )

    class Meta:
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text[:15]


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        verbose_name='Произведение',
        on_delete=models.CASCADE,
        related_name='comments',
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор комментария к отзыву',
        on_delete=models.CASCADE,
        related_name='comments',
    )
    text = models.TextField(
        verbose_name='Комментарий', help_text='Текст комментария'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации комментария', auto_now_add=True
    )

    class Meta:
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text[:15]
