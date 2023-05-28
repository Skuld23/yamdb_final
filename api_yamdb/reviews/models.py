from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from reviews.validators import score_validator, year_validator


class User(AbstractUser):
    '''Модель пользователи'''
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'

    ALL_ROLES = (
        ('admin', 'admin'),
        ('moderator', 'moderator'),
        ('user', 'user'),
    )
    role = models.CharField(
        verbose_name='Должность',
        max_length=100,
        choices=ALL_ROLES,
        default='user',
        blank=True
    )

    bio = models.TextField('Данные о пользователе',
                           blank=True,
                           null=True)

    email = models.EmailField(
        verbose_name='Адрес электронной почты',
        unique=True,
        max_length=254,
        blank=False,
        null=False
    )

    username = models.CharField(
        blank=False,
        null=False,
        max_length=150,
        verbose_name='Имя пользователя',
        unique=True,
        validators=[RegexValidator(
            regex=r'^[\w.@+-]+\Z',
            message='Имя пользователя не может содержать недопустимые символы')
        ]
    )
    first_name = models.CharField(
        'Имя',
        max_length=150,
        null=True,
        blank=True
    )
    last_name = models.CharField(
        "Фамилия",
        max_length=150,
        null=True,
        blank=True
    )
    REQUIRED_FIELDS = ['email', ]
    USERNAME_FIELD = 'username'

    class Meta:
        ordering = ('id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username

    @property
    def there_is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def there_is_admin(self):
        return self.role == self.ADMIN or self.is_superuser or self.is_staff

    @property
    def there_is_user(self):
        return self.role == self.USER


class Category(models.Model):
    '''Модель категории'''
    name = models.CharField(max_length=200,
                            unique=True)
    slug = models.SlugField(
        max_length=50,
        unique=True,
        validators=[RegexValidator(
            regex=r'^[-a-zA-Z0-9_]+$',
            message='Slug не может содержать недопустимые символы')
        ]
    )

    class Meta:
        ordering = ('-name',)

    def __str__(self):
        return self.name


class Genre(models.Model):
    '''Модель жанры'''
    name = models.CharField(max_length=200,
                            unique=True)
    slug = models.SlugField(
        max_length=50,
        unique=True,
        validators=[RegexValidator(
            regex=r'^[-a-zA-Z0-9_]+$',
            message='Slug не может содержать недопустимые символы')
        ]
    )

    def __str__(self):
        return self.name


class Title(models.Model):
    '''Модель произведения'''
    name = models.CharField('Имя', max_length=256)
    year = models.PositiveSmallIntegerField(
        'Дата публикации',
        validators=(year_validator,)
    )
    description = models.TextField('Описание', blank=True)
    genre = models.ManyToManyField(Genre,
                                   through='GenreTitle')
    category = models.ForeignKey(Category,
                                 on_delete=models.SET_NULL,
                                 related_name='titles',
                                 blank=True,
                                 null=True)

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    genre = models.ForeignKey(Genre,
                              on_delete=models.SET_NULL,
                              blank=True,
                              null=True)
    title = models.ForeignKey(Title,
                              on_delete=models.SET_NULL,
                              blank=True,
                              null=True)

    def __str__(self):
        return f'{self.genre} {self.title}'


class Review(models.Model):
    '''Модель Отзывы'''
    title = models.ForeignKey('Title',
                              on_delete=models.CASCADE,
                              related_name='reviews',
                              )
    text = models.TextField(max_length=1500)
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='reviews')
    score = models.IntegerField('Рейтинг',
                                validators=(score_validator,)
                                )
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('author', 'title'),
                name='unique_author_title'
            )
        ]

    def __str__(self):
        return self.text[:50]


class Comment(models.Model):
    review = models.ForeignKey(Review,
                               related_name='comments',
                               on_delete=models.CASCADE,)
    text = models.TextField(max_length=1000)
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='comments')
    pub_date = models.DateTimeField('Дата добавления',
                                    auto_now_add=True,
                                    db_index=True)

    def __str__(self):
        return self.text[:50]
