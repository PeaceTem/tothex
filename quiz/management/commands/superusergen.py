from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string

class Command(BaseCommand):

    # django help function - display the help text
    help = 'This command generates a new list of users!'

    def add_arguments(self, parser):
        parser.add_argument('qty', type=int, help='This is the number of the users to be created!')
        parser.add_argument('-a', '--admin', action='store_true', help='Define an adminstrator account!')


    def handle(self, *args, **kwargs):
        qty= kwargs['qty']
        admin= kwargs['admin']
        

        for i in range(qty):
            username = get_random_string(10)
            password = get_random_string(10)

            if admin:

                User.objects.create_superuser(username=username, email='', password=password)
            else:
                User.objects.create_user(username=username, email='', password=password)
            self.stdout.write(f'The username: {username}\nThe password: {password}')
