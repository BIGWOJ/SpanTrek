from django.core.management.base import BaseCommand
from lessons.models import Lesson
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
        lesson_json_data = os.path.join(base_dir, 'data', 'poland', f'{landmark}.json')

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
                    # Try to get existing lesson by landmark and order
                    lesson, created = Lesson.objects.get_or_create(
                        landmark=landmark,
                        order=lesson_data['order'],
                        defaults=lesson_data
                    )

                    if not created:
                        # Check if any data needs updating
                        update_needed = False
                        for key, value in lesson_data.items():
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