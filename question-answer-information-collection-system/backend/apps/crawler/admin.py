from django.contrib import admin
from .models import Question, Answer


class AnswerInline(admin.TabularInline):
    """答案内联显示"""
    model = Answer
    extra = 0
    fields = ('content', 'answerer', 'answer_time', 'source_order')
    readonly_fields = ('created_at',)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    """问题管理"""
    list_display = ('question_id', 'title', 'category', 'answer_count', 'location', 'publish_time', 'created_at')
    search_fields = ('question_id', 'title', 'description', 'category', 'location')
    list_filter = ('category', 'location', 'publish_time', 'created_at', 'crawl_page')
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'publish_time'
    inlines = [AnswerInline]

    fieldsets = (
        ('基本信息', {
            'fields': ('question_id', 'title', 'description')
        }),
        ('元数据', {
            'fields': ('category', 'publish_time', 'location', 'answer_count', 'crawl_page')
        }),
        ('来源信息', {
            'fields': ('source_url',)
        }),
        ('系统信息', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    """答案管理"""
    list_display = ('id', 'question_link', 'answerer', 'answer_time', 'source_order', 'created_at')
    search_fields = ('content', 'answerer', 'question__title')
    list_filter = ('answer_time', 'created_at')
    readonly_fields = ('created_at',)

    def question_link(self, obj):
        """显示问题链接"""
        return obj.question.title[:50]
    question_link.short_description = '问题'
