"""
View для раздачи медиа файлов в продакшене
Временное решение - для продакшена рекомендуется использовать облачное хранилище
"""
from django.http import FileResponse, Http404
from django.conf import settings
from django.views.decorators.cache import cache_control
from pathlib import Path
import os


@cache_control(max_age=3600)
def serve_media(request, path):
    """
    Раздача медиа файлов
    ВАЖНО: На Heroku файловая система эфемерна!
    Медиа файлы будут потеряны при перезапуске приложения.
    Для продакшена используйте облачное хранилище (AWS S3, Cloudinary и т.д.)
    """
    file_path = Path(settings.MEDIA_ROOT) / path
    if file_path.exists() and file_path.is_file():
        return FileResponse(open(file_path, 'rb'))
    raise Http404("File not found")

