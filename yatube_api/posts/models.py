from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()
STR_METHOD_LENGHT = 30


class Group(models.Model):
    """
    Group model class.

    Contains title, slug and description fields.
    """

    title = models.CharField(max_length=200, verbose_name='Название')
    slug = models.SlugField(unique=True, verbose_name='Слаг')
    description = models.TextField(verbose_name='Описание')

    class Meta:
        """Meta class for Group model."""

        verbose_name = 'группа'
        verbose_name_plural = 'Группы'

    def __str__(self):
        """Magic method for Group model."""
        return self.title[:STR_METHOD_LENGHT]


class Post(models.Model):
    """
    Post model class.

    Contains text, pub_date, author, image and group fields.
    """

    text = models.TextField(verbose_name='Текст')
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )
    image = models.ImageField(
        upload_to='posts/',
        null=True, blank=True,
        verbose_name='Изображение'
    )
    group = models.ForeignKey(
        Group, on_delete=models.SET_NULL,
        blank=True, null=True,
        verbose_name='Группа'
    )

    class Meta:
        """Meta class for Post model."""

        default_related_name = 'posts'
        verbose_name = 'пост'
        verbose_name_plural = 'Посты'
        ordering = ('pub_date',)

    def __str__(self):
        """Magic method for Post model."""
        return self.text[:STR_METHOD_LENGHT]


class Comment(models.Model):
    """
    Comment model class.

    Contains author, post, text and created fields.
    """

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        verbose_name='Пост'
    )
    text = models.TextField(verbose_name='Текст')
    created = models.DateTimeField(
        verbose_name='Дата добавления',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        """Meta class for Comment model."""

        default_related_name = 'comments'
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        """Magic method for Comment model."""
        return (f'Комментарий {self.text[:STR_METHOD_LENGHT]} пользователя '
                f'{self.author} под постом {self.post.pk}')


class Follow(models.Model):
    """
    Follow model class.

    Contains user and following fields.
    """

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='follows'
    )
    following = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Подписка',
        related_name='following'
    )

    class Meta:
        """Meta class for Follow model."""

        verbose_name = 'подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'following'],
                name='unique_user_following'
            )
        ]

    def __str__(self):
        """Magic method for Follow model."""
        return f'Пользователь {self.user} подписан на {self.following}'
