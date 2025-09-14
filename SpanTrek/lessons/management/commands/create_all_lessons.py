from django.core.management.base import BaseCommand
from django.core.management import call_command
from io import StringIO
from django.core.management.base import OutputWrapper
from contextlib import redirect_stdout
import re

class Command(BaseCommand):
    help = 'Creates all Spanish lessons across Polish cities in the correct learning order'

    def extract_statistics(self, output):
        """Extract statistics from command output"""
        created = sum(int(x) for x in re.findall(r'Created: (\d+)', output))
        updated = sum(int(x) for x in re.findall(r'Updated: (\d+)', output))
        skipped = sum(int(x) for x in re.findall(r'Skipped: (\d+)', output))
        return created, updated, skipped

    def handle(self, *args, **kwargs):
        # The order of cities matches the Spanish learning progression
        cities = [
            'szczecin',
            'krakow',
            'gdansk',
            'poznan',
            'warsaw'
        ]

        # Track overall statistics
        total_created = 0
        total_updated = 0
        total_skipped = 0
        processed_cities = 0

        for city in cities:
            self.stdout.write(f'\nProcessing Spanish lessons for {city.title()}...')
            try:
                # Capture output from create_city_lessons command
                output = StringIO()
                with redirect_stdout(output):
                    call_command('create_city_lessons', city)
                
                # Print the captured output
                output_str = output.getvalue()
                self.stdout.write(output_str)
                
                # Extract statistics from the output
                created, updated, skipped = self.extract_statistics(output_str)
                total_created += created
                total_updated += updated
                total_skipped += skipped
                processed_cities += 1

            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'Error processing lessons for {city}: {str(e)}')
                )
                raise

        # Print overall summary
        self.stdout.write('\n' + '='*50)
        self.stdout.write(self.style.SUCCESS('Overall Lesson Import Summary:'))
        self.stdout.write(f'Cities processed: {processed_cities}')
        self.stdout.write(self.style.SUCCESS(f'Total lessons created: {total_created}'))
        self.stdout.write(self.style.WARNING(f'Total lessons updated: {total_updated}'))
        self.stdout.write(f'Total lessons skipped: {total_skipped}')
        self.stdout.write(
            self.style.SUCCESS(f'Total lessons processed: {total_created + total_updated + total_skipped}')
        )