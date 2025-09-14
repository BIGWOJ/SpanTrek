from django.core.management.base import BaseCommand
from lessons.models import Sentence
from django.db import IntegrityError
import json
import os

class Command(BaseCommand):
    help = 'Creates sentence entries from the sentences.json file'

    def handle(self, *args, **options):
        # Get the path to the sentences data file
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        sentences_json_data = os.path.join(base_dir, 'data', 'sentences.json')

        if not os.path.exists(sentences_json_data):
            self.stdout.write(self.style.ERROR('No sentences data file found'))
            return

        try:
            # Read the sentences data
            with open(sentences_json_data, 'r', encoding='utf-8') as f:
                sentences_data = json.load(f)

            # Track statistics
            created_count = 0
            skipped_count = 0
            updated_count = 0

            # Create or update sentence entries
            for entry in sentences_data:
                spanish_sentence = entry['sentence']
                try:
                    # Try to get existing entry
                    sentence_entry, created = Sentence.objects.get_or_create(
                        sentence=spanish_sentence,
                        defaults={
                            'translation': entry['translation']
                        }
                    )

                    # If entry exists but translation is different, update it
                    if not created:
                        if sentence_entry.translation != entry['translation']:
                            sentence_entry.translation = entry['translation']
                            sentence_entry.save()
                            updated_count += 1
                            self.stdout.write(
                                self.style.WARNING(f'Updated sentence entry: {spanish_sentence}')
                            )
                        else:
                            skipped_count += 1
                            self.stdout.write(f'Skipped existing sentence entry: {spanish_sentence}')
                    else:
                        created_count += 1
                        self.stdout.write(
                            self.style.SUCCESS(f'Created sentence entry: {spanish_sentence}')
                        )

                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f'Error processing sentence entry for {spanish_sentence}: {str(e)}')
                    )

            # Print summary
            self.stdout.write('\nSentence import summary:')
            self.stdout.write(self.style.SUCCESS(f'Created: {created_count}'))
            self.stdout.write(self.style.WARNING(f'Updated: {updated_count}'))
            self.stdout.write(f'Skipped: {skipped_count}')
            self.stdout.write(self.style.SUCCESS(f'Total processed: {created_count + updated_count + skipped_count}'))

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error processing sentences data: {str(e)}')
            )
            raise