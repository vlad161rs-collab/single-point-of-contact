from django.core.management.base import BaseCommand
from portal.models import Department


class Command(BaseCommand):
    help = 'Создает отделы компании'

    def handle(self, *args, **options):
        departments = [
            'Научный отдел',
            'Отдел технической поддержки',
            'Отдел проектирования',
            'Отдел кадров',
            'Юридический отдел',
            'Отдел бухгалтерии',
            'Отдел продаж',
        ]

        created_count = 0
        for dept_name in departments:
            department, created = Department.objects.get_or_create(name=dept_name)
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Создан отдел: {dept_name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Отдел уже существует: {dept_name}')
                )

        self.stdout.write(
            self.style.SUCCESS(
                f'\nВсего создано отделов: {created_count} из {len(departments)}'
            )
        )







