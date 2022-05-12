from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string

class Command(BaseCommand):

    # django help function - display the help text
    help = 'This command dletes a list of users!'

    def add_arguments(self, parser):
        parser.add_argument('user_id', nargs='+', type=int, help="Supply the user's id")

    def handle(self, *args, **kwargs):
        users= kwargs['user_id']


        for user_id in users:
            try:
                user = User.objects.get(id=user_id)
                user.delete()
                self.stdout.write(f"{user.username} has been deleted!")
            except User.DoesNotExist:
                self.stdout.write(f'The user with id {user_id} does not exists in the database.')
