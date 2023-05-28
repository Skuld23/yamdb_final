from django.contrib import admin

from .models import Category, Comment, Genre, GenreTitle, Review, Title, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'username',
        'email',
        'first_name',
        'last_name',
        'bio',
        'role',
    )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'slug',
    )
    prepopulated_fields = {'slug': ('name',), }
    empty_value_display = '-пусто-'


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'slug',
    )
    prepopulated_fields = {'slug': ('name',), }
    empty_value_display = '-пусто-'


@admin.register(Title)
class TitlesAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'year',
        'description',
        'category',
    )
    search_fields = ('description',)
    list_filter = ('year',)
    empty_value_display = '-пусто-'


@admin.register(GenreTitle)
class GenreTitlesAdmin(admin.ModelAdmin):
    list_display = (
        'genre',
        'title',
    )
    empty_value_display = '-пусто-'


@admin.register(Review)
class ReviewsAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'text',
        'author',
        'score',
        'pub_date',
    )
    list_editable = ('role',)
    list_filter = ('username', 'role',)
    search_fields = ('username', 'role',)
    list_editable = ('score',)
    search_fields = ('text',)
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'


@admin.register(Comment)
class CommentsAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'text',
        'author',
        'pub_date',
    )
    list_editable = ('text',)
    search_fields = ('text',)
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'
