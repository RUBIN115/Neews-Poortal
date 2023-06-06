from django.contrib import admin
from .models import Author, Category, Post, PostCategory, Comment

def nullfy_quantity_news(modeladmin, request, queryset):
    queryset.update(quantity=0)
nullfy_quantity_news.short_description = 'Обнулить новости'

class PostsAdmin(admin.ModelAdmin):
    list_display = ('author', 'type', 'date_time_create', 'category', 'post_rating')
    list_filter = ('date_time_create', 'quantity', 'title', 'author')
    search_fields = ('author', 'category__author')
    actions = [nullfy_quantity_news]


def nullfy_quantity_author(modeladmin, request, queryset):
    queryset.update(quantity=0)
nullfy_quantity_author.short_description = 'Обнулить авторов'

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('user', 'author_rating', 'quantity')
    list_filter = ('user', 'author_rating')
    search_fields = ('user')
    actions = [nullfy_quantity_author]


def nullfy_quantity_category(modeladmin, request, queryset):
    queryset.update(quantity=0)
nullfy_quantity_category.short_description = 'Обнулить категории'

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'quantity')
    list_filter = ('name', 'quantity')
    search_fields = ('name')
    actions = [nullfy_quantity_category]


def nullfy_quantity_comments(modeladmin, request, queryset):
    queryset.update(quantity=0)
nullfy_quantity_comments.short_description = 'Обнулить комментарии'

class CommentAdmin(admin.ModelAdmin):
    list_display = ('date_time_create', 'comment_rating', 'quantity')
    list_filter = ('date_time_create', 'comment_rating', 'quantity')
    search_fields = ('date_time_create')
    actions = [nullfy_quantity_comments]



admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Post)
admin.site.register(PostCategory)
admin.site.register(Comment)