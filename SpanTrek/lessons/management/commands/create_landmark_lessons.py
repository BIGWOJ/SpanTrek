from django.core.management.base import BaseCommand
from lessons.models import Lesson, Country
import json
import os

class Command(BaseCommand):
    help = 'Creates Spanish lessons for a specific landmark'

    def add_arguments(self, parser):
        parser.add_argument('landmark', type=str, help='Name of the landmark')

    def handle(self, *args, **options):
        landmark = options['landmark'].lower()
        
        # Get the path to the lesson data file
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        lesson_json_data = os.path.join(base_dir, 'landmark_data', 'poland', f'{landmark}.json')

        if not os.path.exists(lesson_json_data):
            self.stdout.write(self.style.ERROR(f'No lesson data found for {landmark}'))
            return

        try:
            with open(lesson_json_data, 'r', encoding='utf-8') as f:
                lessons_data = json.load(f)

            # Track statistics
            created_count = 0
            skipped_count = 0
            updated_count = 0

            for lesson_data in lessons_data:
                try:
                    # Remove ManyToMany fields and country from defaults
                    defaults = {k: v for k, v in lesson_data.items() if k not in ['vocabularies', 'sentences', 'country']}

                    country_obj = Country.objects.filter(name=lesson_data['country']).first()

                    # Try to get existing lesson by landmark and order
                    lesson, created = Lesson.objects.get_or_create(
                        landmark=landmark,
                        country=country_obj,
                        order=lesson_data['order'],
                        defaults=defaults
                    )

                    if not created:
                        # Check if any data needs updating
                        update_needed = False
                        for key, value in lesson_data.items():
                                if key not in ['vocabularies', 'sentences']:
                                    if getattr(lesson, key) != value:
                                        setattr(lesson, key, value)
                                        update_needed = True

                        if update_needed:
                            lesson.save()
                            updated_count += 1
                            self.stdout.write(
                                self.style.WARNING(f'Updated lesson: {lesson.title} (Order: {lesson.order})')
                            )
                        else:
                            skipped_count += 1
                            self.stdout.write(f'Skipped existing lesson: {lesson.title} (Order: {lesson.order})')
                    else:
                        created_count += 1
                        self.stdout.write(
                            self.style.SUCCESS(f'Created lesson: {lesson.title} (Order: {lesson.order})')
                        )

                        # Assign vocabularies ManyToMany
                        vocab_objs = []
                        for vocab in lesson_data.get('vocabularies', []):
                            vocab_obj, _ = lesson.vocabularies.model.objects.get_or_create(
                                word=vocab['word'],
                                defaults={
                                    'translation': vocab.get('translation', ''),
                                    'pronunciation': vocab.get('pronunciation', ''),
                                    'example_sentence': vocab.get('example_sentence', ''),
                                    'conjugation': vocab.get('conjugation', ''),
                                    'audio_url': vocab.get('audio_url', '')
                                }
                            )
                            vocab_objs.append(vocab_obj)
                        lesson.vocabularies.set(vocab_objs)

                        # Assign sentences ManyToMany
                        sentence_objs = []
                        for sent in lesson_data.get('sentences', []):
                            sent_obj, _ = lesson.sentences.model.objects.get_or_create(
                                sentence=sent['sentence'],
                                defaults={
                                    'translation': sent.get('translation', '')
                                }
                            )
                            sentence_objs.append(sent_obj)
                        lesson.sentences.set(sentence_objs)
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f'Error processing lesson (Order: {lesson_data.get("order")}): {str(e)}')
                    )

            # Print summary for this landmark
            self.stdout.write(f'\nLesson import summary for {landmark.title()}:')
            self.stdout.write(self.style.SUCCESS(f'Created: {created_count}'))
            self.stdout.write(self.style.WARNING(f'Updated: {updated_count}'))
            self.stdout.write(f'Skipped: {skipped_count}')
            self.stdout.write(
                self.style.SUCCESS(f'Total processed: {created_count + updated_count + skipped_count}')
            )

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error creating lessons for {landmark}: {str(e)}')
            )
            raise