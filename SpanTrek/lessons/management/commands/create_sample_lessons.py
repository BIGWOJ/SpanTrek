from django.core.management.base import BaseCommand
from lessons.models import Lesson


class Command(BaseCommand):
    help = 'Create sample lessons for testing'

    def handle(self, *args, **options):
        # Przykładowe lekcje
        lessons_data = [
            {
                'title': 'Basic Greetings',
                'description': 'Learn how to say hello, goodbye, and basic polite expressions in Spanish.',
                'level': 1,
                'order': 1,
            },
            {
                'title': 'Numbers 1-20',
                'description': 'Master the Spanish numbers from one to twenty.',
                'level': 1,
                'order': 2,
            },
            {
                'title': 'Days of the Week',
                'description': 'Learn the seven days of the week in Spanish.',
                'level': 1,
                'order': 3,
            },
            {
                'title': 'Family Members',
                'description': 'Learn vocabulary related to family relationships.',
                'level': 2,
                'order': 4,
            },
            {
                'title': 'Colors',
                'description': 'Learn the basic colors in Spanish.',
                'level': 2,
                'order': 5,
            },
            {
                'title': 'Present Tense Verbs',
                'description': 'Introduction to present tense conjugation of regular verbs.',
                'level': 3,
                'order': 6,
            },
        ]

        for lesson_data in lessons_data:
            lesson, created = Lesson.objects.get_or_create(
                title=lesson_data['title'],
                defaults=lesson_data
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Created lesson: {lesson.title}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Lesson already exists: {lesson.title}')
                )

        self.stdout.write(
            self.style.SUCCESS('Sample lessons created successfully!')
        )
