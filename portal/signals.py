from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db import OperationalError, ProgrammingError
from .models import UserProfile


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Автоматически создаем профиль при создании пользователя"""
    if not created:
        return

    try:
        UserProfile.objects.get_or_create(user=instance)
    except (OperationalError, ProgrammingError):
        # Во время первого деплоя таблицы portal могут еще создаваться миграциями.
        return







