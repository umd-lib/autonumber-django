import csv

from django.core.management.base import BaseCommand
from django.db import transaction

from autonumber.ui.models import AutoNumber, CollectingArea, User


class Command(BaseCommand):
  help = 'Imports legacy data from CSV files'

  def add_arguments(self, parser):
    parser.add_argument('repositories', type=str, help='Path to the repositories CSV file (e.g., repositories.csv)')
    parser.add_argument('names', type=str, help='Path to the names CSV file (e.g., names.csv)')
    parser.add_argument('auto_numbers', type=str, help='Path to the auto_numbers CSV file (e.g., auto_numbers.csv)')
    parser.add_argument('users', type=str, help='Path to the users CSV file (e.g., users.csv)')

  def _read_csv(self, filename):
    try:
      with open(filename) as file:
        dict_reader = csv.DictReader(file)
        return list(dict_reader)
    except FileNotFoundError:
      self.stdout.write(self.style.ERROR(f'File not found: {filename}'))
      return None
    except Exception as e:
      self.stdout.write(self.style.ERROR(f'Error reading {filename}: {e}'))
      return None

  def handle(self, *args, **options):
    repo_dict = self._read_csv(options.get('repositories', 'repositories.csv'))
    name_dict = self._read_csv(options.get('names', 'names.csv'))
    number_dict = self._read_csv(options.get('auto_numbers', 'auto_numbers.csv'))
    user_dict = self._read_csv(options.get('users', 'users.csv'))

    if any(file is None for file in [repo_dict, name_dict, number_dict, user_dict]):
      self.stdout.write(self.style.ERROR('Aborting import due to missing file(s).'))
      return

    with transaction.atomic():
      self.stdout.write(self.style.SUCCESS('Starting data import...'))

      self.stdout.write('Importing CollectingArea...')
      collecting_areas = [
        CollectingArea(
          name=row['name'],
        )
        for row in repo_dict
      ]
      CollectingArea.objects.bulk_create(collecting_areas)
      self.stdout.write(self.style.SUCCESS(f'Successfully imported {len(collecting_areas)} CollectingArea records.'))

      name_lookup = {row['id']: row['initials'] for row in name_dict}

      self.stdout.write('Importing AutoNumber...')
      auto_numbers = []
      for row in number_dict:
        creator_name = name_lookup.get(row['name_id'], 'n/a')

        try:
          collecting_area = CollectingArea.objects.get(id=row['repository_id'])
        except CollectingArea.DoesNotExist:
          self.stdout.write(
            self.style.ERROR(f'Skipping AutoNumber ID {row["id"]}: CollectionArea ID {row["repository_id"]} not found.')
          )
          continue

        auto_numbers.append(
          AutoNumber(
            id=row['id'],
            entry_date=row['entry_date'],
            name=creator_name,
            collecting_area=collecting_area,
          )
        )

      AutoNumber.objects.bulk_create(auto_numbers)
      self.stdout.write(self.style.SUCCESS(f'Successfully imported {len(auto_numbers)} AutoNumber records.'))

      self.stdout.write('Importing Users...')
      users = []
      for row in user_dict:
        clean_name = row['name'].strip().replace('"', '')

        users.append(
          User(
            cas_directory_id=row['cas_directory_id'],
            name=clean_name,
          )
        )

      User.objects.bulk_create(users)
      self.stdout.write(self.style.SUCCESS(f'Successfully imported {len(users)} User records.'))

    self.stdout.write(self.style.SUCCESS('All legacy data import completed successfully!'))
