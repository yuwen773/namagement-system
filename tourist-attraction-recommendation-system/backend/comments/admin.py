from django.contrib import admin
from .models import Comment, Favorite


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'attraction', 'rating', 'status', 'created_at']
    list_filter = ['status', 'rating']
    search_fields = ['content']


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'attraction', 'created_at']
