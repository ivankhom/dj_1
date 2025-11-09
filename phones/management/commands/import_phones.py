import csv

from django.core.management import BaseCommand

from phones.models import Phone


class Command(BaseCommand):
    help = 'Import phones from CSV file'

    def handle(self, *args, **options):
        csv_file_path = 'phones.csv'

        with open(csv_file_path, 'r', encoding='utf-8') as file:
            phones = list(csv.DictReader(file, delimiter=';'))

            for phone_data in phones:
                try:
                    Phone.objects.create(
                        name=phone_data['name'],
                        price=float(phone_data['price']),
                        image=phone_data['image'],
                        release_date=phone_data['release_date'],
                        lte_exists=phone_data['lte_exists'].lower() == 'true'
                    )
                    self.stdout.write(
                        self.style.SUCCESS(f'Successfully added {phone_data["name"]}')
                    )
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f'Error adding {phone_data["name"]}: {str(e)}')
                    )

        self.stdout.write(
            self.style.SUCCESS(f'Successfully imported {len(phones)} phones')
        )