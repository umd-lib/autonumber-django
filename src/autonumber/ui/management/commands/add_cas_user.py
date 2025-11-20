from django.core.management.base import BaseCommand, CommandError

from autonumber.ui.models import User


class Command(BaseCommand):
  help = 'Add a user, specifying their CAS directory ID and full name.'

  def add_arguments(self, parser):
    parser.add_argument('id', type=str, help='The unique CAS directory ID for the user.')
    parser.add_argument('name', type=str, help='The full name of the user.')

  def handle(self, *args, **options):
    cas_directory_id = options['id']
    name = options['name']

    try:
      _, created = User.objects.get_or_create(
        cas_directory_id=cas_directory_id,
        name=name
      )

      if created:
        self.stdout.write(self.style.SUCCESS(f"User '{cas_directory_id}' created!"))
      else:
        self.stdout.write(f"User '{cas_directory_id}' already exists!")

    except Exception as e:
      raise CommandError(f'An error occurred: {e}')
