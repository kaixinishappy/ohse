from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from users.models import UserRole 

class Command(BaseCommand):
    help = "Create groups for each user role"

    def handle(self, *args, **kwargs):
        for role, _ in UserRole.choices:
            group, created = Group.objects.get_or_create(name=role)
            if created:
                self.stdout.write(self.style.SUCCESS(f"Group '{role}' created"))
            else:
                self.stdout.write(self.style.WARNING(f"Group '{role}' already exists"))
