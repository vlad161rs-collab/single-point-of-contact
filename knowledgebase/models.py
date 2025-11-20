from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone


class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='articles/images/', blank=True, null=True)
    video = models.FileField(upload_to='articles/videos/', blank=True, null=True)
    audio = models.FileField(upload_to='articles/audios/', blank=True, null=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='articles',
        verbose_name='Автор'
    )

    class Meta:
        ordering = ['-pub_date']
        indexes = [
            models.Index(fields=['-pub_date']),
            models.Index(fields=['title']),
            models.Index(fields=['author']),
        ]
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'

    def __str__(self):
        return self.title


class Request(models.Model):
    STATUS_CHOICES = [
        ('New', 'Новая'),
        ('In Progress', 'В работе'),
        ('Completed', 'Завершена'),
        ('Cancelled', 'Отменена'),
    ]

    CATEGORY_CHOICES = [
        ('Technical', 'Техническая'),
        ('Content', 'Контент'),
        ('Other', 'Другое'),
        ('Uncategorized', 'Без категории'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
        default='Uncategorized'
    )
    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default='New'
    )
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='requests',
        verbose_name='Создатель'
    )

    class Meta:
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['category']),
            models.Index(fields=['created_by']),
        ]
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'

    def __str__(self):
        return self.title


class Comment(models.Model):
    text = models.TextField()
    article = models.ForeignKey(
        'Article',
        related_name='comments',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    request = models.ForeignKey(
        'Request',
        related_name='comments',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comments',
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['created_at']),
            models.Index(fields=['article']),
            models.Index(fields=['request']),
        ]
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def clean(self):
        """Ensure comment is associated with either article or request, but not both."""
        if not self.article and not self.request:
            raise ValidationError('Комментарий должен быть привязан к статье или заявке.')
        if self.article and self.request:
            raise ValidationError('Комментарий не может быть привязан одновременно к статье и заявке.')

    def save(self, *args, **kwargs):
        if self.article or self.request:
            self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.text[:50]


