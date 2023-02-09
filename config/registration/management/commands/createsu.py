from registration.models import User
from django.core.management.base import BaseCommand
from django.conf import settings

class Command(BaseCommand):
    help = 'Creates a superuser.'

    def handle(self, *args, **options):
        # print(settings.SUPERUSER_EMAIL, settings.SUPERUSER_PASSWORD)
        if not User.objects.filter(email=settings.SUPERUSER_EMAIL).exists():
            User.objects.create_superuser(
                email=settings.SUPERUSER_EMAIL,
                password=settings.SUPERUSER_PASSWORD
            )
        print('Superuser has been created.')
    # def handle(self, *args, **options):
    #     print(settings.SUPERUSER_EMAIL, settings.SUPERUSER_PASSWORD)
    #     if not User.objects.filter(email=settings.SUPERUSER_EMAIL).exists():
    #         User.objects.create_superuser(
    #             email=settings.SUPERUSER_EMAIL,
    #             password=settings.SUPERUSER_PASSWORD
    #         )
    #     print('Superuser has been created.')