from django.contrib import admin
from .models import Article, Request, Comment


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'pub_date', 'has_image', 'has_video', 'has_audio')
    search_fields = ('title', 'content', 'author__username', 'author__email')
    list_filter = ('pub_date', 'author')
    ordering = ('-pub_date',)
    readonly_fields = ('pub_date',)
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'content', 'author', 'pub_date')
        }),
        ('Медиа файлы', {
            'fields': ('image', 'video', 'audio'),
            'classes': ('collapse',)
        }),
    )

    def has_image(self, obj):
        return bool(obj.image)
    has_image.boolean = True
    has_image.short_description = 'Изображение'

    def has_video(self, obj):
        return bool(obj.video)
    has_video.boolean = True
    has_video.short_description = 'Видео'

    def has_audio(self, obj):
        return bool(obj.audio)
    has_audio.boolean = True
    has_audio.short_description = 'Аудио'


@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_by', 'category', 'status', 'created_at', 'updated_at', 'comment_count')
    list_filter = ('status', 'category', 'created_at', 'created_by')
    search_fields = ('title', 'description', 'created_by__username', 'created_by__email')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'description', 'category', 'status', 'created_by')
        }),
        ('Даты', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def comment_count(self, obj):
        return obj.comments.count()
    comment_count.short_description = 'Комментариев'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('text_preview', 'user', 'article', 'request', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('text', 'user__username')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)

    def text_preview(self, obj):
        return obj.text[:50] + '...' if len(obj.text) > 50 else obj.text
    text_preview.short_description = 'Текст'
