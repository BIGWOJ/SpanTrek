from django.core.management.base import BaseCommand
from lessons.models import Lesson, Country, Landmark, Audio
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
                    # Remove ManyToMany fields and ForeignKey fields from defaults
                    defaults = {k: v for k, v in lesson_data.items() if k not in ['vocabularies', 'sentences', 'country', 'landmark']}

                    # Get the country object
                    country_obj = Country.objects.filter(name=lesson_data['country']).first()
                    if not country_obj:
                        self.stdout.write(
                            self.style.ERROR(f'Country "{lesson_data["country"]}" not found. Please create it first.')
                        )
                        continue

                    # Get or create the landmark object
                    landmark_obj, landmark_created = Landmark.objects.get_or_create(
                        name=landmark,
                        country=country_obj,
                        defaults={}
                    )
                    
                    if landmark_created:
                        self.stdout.write(
                            self.style.SUCCESS(f'Created landmark: {landmark_obj}')
                        )

                    # Try to get existing lesson by landmark and order
                    lesson, created = Lesson.objects.get_or_create(
                        landmark=landmark_obj,
                        order=lesson_data['order'],
                        defaults={**defaults, 'country': country_obj}
                    )

                    if not created:
                        # Check if any data needs updating
                        update_needed = False
                        for key, value in lesson_data.items():
                            if key not in ['vocabularies', 'sentences', 'country', 'landmark']:
                                if getattr(lesson, key) != value:
                                    setattr(lesson, key, value)
                                    update_needed = True
                        
                        # Also check if country needs updating
                        if lesson.country != country_obj:
                            lesson.country = country_obj
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

                        # Update ManyToMany relationships for existing lessons
                        # Update vocabularies
                        vocab_objs = []
                        for vocab in lesson_data.get('vocabularies', []):
                            vocab_obj, _ = lesson.vocabularies.model.objects.get_or_create(
                                word=vocab['word'],
                                defaults={
                                    'translation': vocab.get('translation', '')
                                }
                            )
                            vocab_objs.append(vocab_obj)
                        lesson.vocabularies.set(vocab_objs)

                        # Update sentences
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

                        # Update audio
                        audio_objs = []
                        lesson_sequence = lesson_data.get('lesson_sequence', [])
                        
                        for item in lesson_sequence:
                            audio_data = item.get('content', [])
                            if len(audio_data) >= 2:
                                audio_url = audio_data[0]
                                audio_text = audio_data[1]
                                
                                audio_obj, _ = Audio.objects.get_or_create(
                                    audio_url=audio_url,
                                    defaults={'text': audio_text}
                                )
                                audio_objs.append(audio_obj)
                        
                        lesson.audios.set(audio_objs)
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
                                    'translation': vocab.get('translation', '')
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

                        # Assign audio ManyToMany
                        audio_objs = []
                        lesson_sequence = lesson_data.get('lesson_sequence', [])

                        for item in lesson_sequence:
                            if isinstance(item, dict) and item.get('type') == 'audio':
                                audio_data = item.get('content', [])
                                if len(audio_data) >= 2:
                                    audio_url = audio_data[0]
                                    audio_text = audio_data[1]
                                    
                                    audio_obj, _ = Audio.objects.get_or_create(
                                        audio_url=audio_url,
                                        defaults={'text': audio_text}
                                    )
                                    audio_objs.append(audio_obj)
                        lesson.audios.set(audio_objs)
                        
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