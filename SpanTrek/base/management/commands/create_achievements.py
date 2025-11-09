from django.core.management.base import BaseCommand
from base.models import Achievement

class Command(BaseCommand):
    help = 'Create default achievements for the application'

    def handle(self, *args, **options):
        achievements_data = [
            # Streak
            {
                'code': 'streak_3',
                'name': 'Streak Beginner',
                'description': 'Reach streak of 3 days',
                'icon': '🔥',
                'experience_award': 75,
            },
            {
                'code': 'streak_7',
                'name': 'Streak Master',
                'description': 'Reach streak of 7 days',
                'icon': '🔥',
                'experience_award': 150,
            },
            {
                'code': 'streak_30',
                'name': 'Streak Legend',
                'description': 'Reach streak of 30 days',
                'icon': '🔥',
                'experience_award': 500,
            },
            # Levels
            {
                'code': 'level_2',
                'name': 'Baby Step',
                'description': 'Reach level 2',
                'icon': '👶🏼',
                'experience_award': 50,
            },
            {
                'code': 'level_5',
                'name': 'Level Up',
                'description': 'Reach level 5',
                'icon': '🎖️',
                'experience_award': 100,
            },
            {
                'code': 'level_10',
                'name': 'Expert',
                'description': 'Reach level 10',
                'icon': '🏆',
                'experience_award': 250,
            },
            {
                'code': 'level_20',
                'name': 'Master',
                'description': 'Reach level 20',
                'icon': '👑',
                'experience_award': 500,
            },
            # Experience
            {
                'code': 'experience_250',
                'name': 'Getting Started',
                'description': 'Earn your first 250 experience points',
                'icon': '🎯',
                'experience_award': 25,
            },           
            {
                'code': 'experience_2500',
                'name': 'Experience Seeker',
                'description': 'Earn 2500 experience points',
                'icon': '💎',
                'experience_award': 100,
            },
            {
                'code': 'experience_5000',
                'name': 'Experience Master',
                'description': 'Earn 5000 experience points',
                'icon': '💎',
                'experience_award': 300,
            },
            # Adventure
            {
                'code': 'adventure_1',
                'name': 'Adventure Hero',
                'description': 'Complete your first adventure lesson',
                'icon': '🗺️',
                'experience_award': 150,
            },
            {
                'code': 'adventure_poland_50',
                'name': 'Poland Explorer',
                'description': 'Complete 50% of an adventure in Poland',
                'icon': '🇵🇱',
                'experience_award': 125,
            },
            {
                'code': 'adventure_poland_complete',
                'name': 'Poland Master',
                'description': 'Complete adventure in Poland',
                'icon': '🇵🇱',
                'experience_award': 500,
            },
            {
                'code': 'adventure_spain_50',
                'name': 'Spain Explorer',
                'description': 'Complete 50% of an adventure in Spain',
                'icon': '🇪🇸',
                'experience_award': 125,
            },
            {
                'code': 'adventure_spain_complete',
                'name': 'Spain Master',
                'description': 'Complete adventure in Spain',
                'icon': '🇪🇸',
                'experience_award': 500,
            },
            # Time-based
            {
                'code': 'lesson_before_10',
                'name': 'Early Bird',
                'description': 'Study before 10 AM',
                'icon': '🐦',
                'experience_award': 75,
            },
            {
                'code': 'lesson_after_22',
                'name': 'Night Owl',
                'description': 'Study after 10 PM',
                'icon': '🦉',
                'experience_award': 75,
            },
            # Knowledge-based
            {
                'code': 'vocabulary_100',
                'name': 'Word Master',
                'description': 'Learn 100 words',
                'icon': '📚',
                'experience_award': 250,
            },
            {
                'code': 'sentence_25',
                'name': 'Sentence Master',
                'description': 'Learn 25 sentences',
                'icon': '📖',
                'experience_award': 250,
            },
            {
                'code': 'audio_25',
                'name': 'Audiofile',
                'description': 'Learn 25 audio clips',
                'icon': '👂🏻',
                'experience_award': 250,
            },
            {
                'code': 'use_of_spanish_50',
                'name': 'Spanish User',
                'description': 'Reach Use of Spanish to 50%',
                'icon': '📜',
                'experience_award': 250,
            },
        ]

        created_count = 0
        for achievement_data in achievements_data:
            achievement, created = Achievement.objects.get_or_create(
                name=achievement_data['name'],
                defaults=achievement_data
            )
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Created achievement: {achievement.name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Achievement already exists: {achievement.name}')
                )

        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {created_count} new achievements')
        )
