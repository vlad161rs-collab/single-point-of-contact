import shutil
import datetime
from pathlib import Path
from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Создание резервной копии базы данных'

    def handle(self, *args, **kwargs):
        now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        db_path = Path(settings.DATABASES['default']['NAME'])
        backup_dir = Path(settings.BASE_DIR) / 'backups'
        backup_dir.mkdir(exist_ok=True)
        
        # Get database filename without path
        db_filename = db_path.name
        backup_file = backup_dir / f"{db_filename}_backup_{now}.sqlite3"

        if db_path.exists():
            try:
                shutil.copy2(db_path, backup_file)
                self.stdout.write(
                    self.style.SUCCESS(f"Резервная копия создана: {backup_file}")
                )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f"Ошибка при создании резервной копии: {e}")
                )
        else:
            self.stdout.write(
                self.style.ERROR(f"База данных не найдена: {db_path}")
            )
