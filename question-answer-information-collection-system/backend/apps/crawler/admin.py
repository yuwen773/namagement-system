from django.contrib import admin
from .models import Tag, Question


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at')
    search_fields = ('name',)
    list_filter = ('created_at',)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'answerer', 'answer_time', 'created_at')
    search_fields = ('title', 'answer_content', 'answerer')
    list_filter = ('created_at', 'answer_time')
    filter_horizontal = ('tags',)
    raw_id_fields = ('tags',)
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'created_at'
