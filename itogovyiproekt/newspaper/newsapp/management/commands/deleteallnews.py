from django.core.management.base import BaseCommand, CommandError

from newsapp.models import Post


class Command(BaseCommand):
    help = 'Удаляет все новости после подтверждения'

    def handle(self, *args, **options):
        self.stdout.write('Do you really want to delete all news? yes/no')
        answer = input()
        if answer == 'yes':
            Post.objects.filter(choice='N').delete()
            self.stdout.write(self.style.SUCCESS('Succesfully wiped news'))
            return

        self.stdout.write(self.style.ERROR('Access denied'))

