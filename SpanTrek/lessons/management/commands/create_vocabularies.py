from django.core.management.base import BaseCommand
from lessons.models import Vocabulary
import json
import os

class Command(BaseCommand):
    help = 'Creates vocabulary entries from the vocabulary.json file'

    def handle(self, *args, **options):
        # Get the path to the vocabulary data file
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        vocabulary_json_data = os.path.join(base_dir, 'landmark_data', 'vocabulary.json')

        if not os.path.exists(vocabulary_json_data):
            self.stdout.write(self.style.ERROR('No vocabulary data file found'))
            return

        try:
            # Read the vocabulary data
            with open(vocabulary_json_data, 'r', encoding='utf-8') as f:
                vocabulary_data = json.load(f)

            # Track statistics
            created_count = 0
            skipped_count = 0
            updated_count = 0

            # Create or update vocabulary entries
            for entry in vocabulary_data:
                word = entry['word']
                try:
                    # Try to get existing entry
                    vocab_entry, created = Vocabulary.objects.get_or_create(
                        word=word,
                        defaults={
                            'translation': entry['translation'],
                            'pronunciation': entry.get('pronunciation', ''),
                            'example_sentence': entry.get('example_sentence', ''),
                            "conjugation": entry.get('conjugation', ''),
                        }
                    )

                    # If entry exists but data is different, update it
                    if not created:
                        updated = False
                        if vocab_entry.translation != entry['translation']:
                            vocab_entry.translation = entry['translation']
                            updated = True
                        if vocab_entry.pronunciation != entry.get('pronunciation', ''):
                            vocab_entry.pronunciation = entry.get('pronunciation', '')
                            updated = True
                        
                        if updated:
                            vocab_entry.save()
                            updated_count += 1
                            self.stdout.write(
                                self.style.WARNING(f'Updated vocabulary entry: {word}')
                            )
                        else:
                            skipped_count += 1
                            self.stdout.write(f'Skipped existing vocabulary entry: {word}')
                    else:
                        created_count += 1
                        self.stdout.write(
                            self.style.SUCCESS(f'Created vocabulary entry: {word}')
                        )

                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f'Error processing vocabulary entry for {word}: {str(e)}')
                    )

            # Print summary
            self.stdout.write('\nVocabulary import summary:')
            self.stdout.write(self.style.SUCCESS(f'Created: {created_count}'))
            self.stdout.write(self.style.WARNING(f'Updated: {updated_count}'))
            self.stdout.write(f'Skipped: {skipped_count}')
            self.stdout.write(self.style.SUCCESS(f'Total processed: {created_count + updated_count + skipped_count}'))

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error processing vocabulary data: {str(e)}')
            )
            raise
