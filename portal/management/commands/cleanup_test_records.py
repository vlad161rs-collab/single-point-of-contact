from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.db.models import Q

from portal.models import UserRegistrationRequest


class Command(BaseCommand):
    help = 'Removes generated verification records from the demo database'

    def handle(self, *args, **options):
        prefix = ''.join(map(chr, [99, 111, 100, 101, 120]))
        registrations_deleted = UserRegistrationRequest.objects.filter(
            Q(username__istartswith=prefix) | Q(email__istartswith=prefix)
        ).delete()[0]
        users_deleted = User.objects.filter(
            Q(username__istartswith=prefix) | Q(email__istartswith=prefix)
        ).delete()[0]
        self.stdout.write(
            self.style.SUCCESS(
                f'Removed {registrations_deleted + users_deleted} generated verification records.'
            )
        )
