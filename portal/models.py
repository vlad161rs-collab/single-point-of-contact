from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class Department(models.Model):
    """Модель отдела"""
    name = models.CharField(max_length=100, unique=True, verbose_name='Название отдела')
    description = models.TextField(blank=True, verbose_name='Описание')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Отдел'
        verbose_name_plural = 'Отделы'
        ordering = ['name']

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    """Расширенный профиль пользователя"""
    ROLE_CHOICES = [
        ('user', 'Пользователь'),
        ('moderator', 'Модератор'),
        ('admin', 'Администратор'),
        ('support', 'Служба поддержки'),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name='Пользователь'
    )
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='user',
        verbose_name='Роль'
    )
    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='users',
        verbose_name='Отдел'
    )
    phone = models.CharField(max_length=20, blank=True, verbose_name='Телефон')
    position = models.CharField(max_length=100, blank=True, verbose_name='Должность')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили пользователей'

    def __str__(self):
        return f"{self.user.username} - {self.get_role_display()}"

    @property
    def is_admin(self):
        return self.role == 'admin' or self.user.is_superuser

    @property
    def is_moderator(self):
        return self.role in ['admin', 'moderator'] or self.user.is_staff

    @property
    def is_support(self):
        return self.role in ['admin', 'moderator', 'support']


class UserRegistrationRequest(models.Model):
    """Запрос на регистрацию пользователя (требует одобрения админа)"""
    STATUS_CHOICES = [
        ('pending', 'Ожидает одобрения'),
        ('approved', 'Одобрено'),
        ('rejected', 'Отклонено'),
    ]

    username = models.CharField(max_length=150, unique=True, verbose_name='Имя пользователя')
    email = models.EmailField(verbose_name='Email')
    first_name = models.CharField(max_length=150, blank=True, verbose_name='Имя')
    last_name = models.CharField(max_length=150, blank=True, verbose_name='Фамилия')
    phone = models.CharField(max_length=20, blank=True, verbose_name='Телефон')
    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Отдел'
    )
    position = models.CharField(max_length=100, blank=True, verbose_name='Должность')
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name='Статус'
    )
    requested_role = models.CharField(
        max_length=20,
        choices=UserProfile.ROLE_CHOICES,
        default='user',
        verbose_name='Запрашиваемая роль'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    reviewed_at = models.DateTimeField(null=True, blank=True, verbose_name='Дата рассмотрения')
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reviewed_registrations',
        verbose_name='Рассмотрел'
    )
    rejection_reason = models.TextField(blank=True, verbose_name='Причина отклонения')
    password_hash = models.CharField(max_length=128, blank=True, verbose_name='Хеш пароля')

    class Meta:
        verbose_name = 'Запрос на регистрацию'
        verbose_name_plural = 'Запросы на регистрацию'
        ordering = ['-created_at']
        permissions = [
            ('approve_userregistrationrequest', 'Может одобрять запросы на регистрацию'),
        ]

    def __str__(self):
        return f"{self.username} - {self.get_status_display()}"
