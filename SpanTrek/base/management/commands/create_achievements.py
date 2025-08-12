from django.core.management.base import BaseCommand
from base.models import Achievement

class Command(BaseCommand):
    help = 'Create default achievements for the application'

    def handle(self, *args, **options):
        achievements_data = [
            {
                'name': 'First Steps',
                'description': 'Complete your first lesson',
                'icon': '⭐',
                'experience_award': 50,
            },
            {
                'name': 'Getting Started',
                'description': 'Earn your first 100 experience points',
                'icon': '🎯',
                'experience_award': 25,
            },
            {
                'name': 'Streak Beginner',
                'description': 'Complete 3 days in a row',
                'icon': '🔥',
                'experience_award': 75,
            },
            {
                'name': 'Streak Master',
                'description': 'Complete 7 days in a row',
                'icon': '🔥',
                'experience_award': 150,
            },
            {
                'name': 'Streak Legend',
                'description': 'Complete 30 days in a row',
                'icon': '🔥',
                'experience_award': 500,
            },
            {
                'name': 'Level Up',
                'description': 'Reach level 5',
                'icon': '🎖️',
                'experience_award': 100,
            },
            {
                'name': 'Expert',
                'description': 'Reach level 10',
                'icon': '🏆',
                'experience_award': 250,
            },
            {
                'name': 'Master',
                'description': 'Reach level 20',
                'icon': '👑',
                'experience_award': 500,
            },
            {
                'name': 'Experience Hunter',
                'description': 'Earn 1000 experience points',
                'icon': '💎',
                'experience_award': 100,
            },
            {
                'name': 'Experience Master',
                'description': 'Earn 5000 experience points',
                'icon': '💎',
                'experience_award': 300,
            },
            {
                'name': 'Adventure Starter',
                'description': 'Make progress in your first adventure',
                'icon': '🗺️',
                'experience_award': 75,
            },
            {
                'name': 'Adventure Explorer',
                'description': 'Complete 50% of an adventure',
                'icon': '🗺️',
                'experience_award': 200,
            },
            {
                'name': 'Adventure Hero',
                'description': 'Complete your first adventure',
                'icon': '🗺️',
                'experience_award': 400,
            },
            {
                'name': 'Early Bird',
                'description': 'Log in for 7 consecutive days',
                'icon': '🐦',
                'experience_award': 100,
            },
            {
                'name': 'Night Owl',
                'description': 'Complete a lesson after 10 PM',
                'icon': '🦉',
                'experience_award': 50,
            },
            {
                'name': 'Weekend Warrior',
                'description': 'Complete lessons on both Saturday and Sunday',
                'icon': '⚔️',
                'experience_award': 75,
            },
            {
                'name': 'Perfectionist',
                'description': 'Complete 10 lessons with perfect score',
                'icon': '💯',
                'experience_award': 200,
            },
            {
                'name': 'Speed Learner',
                'description': 'Complete 5 lessons in one day',
                'icon': '⚡',
                'experience_award': 150,
            },
            {
                'name': 'Dedicated Student',
                'description': 'Study for 30 consecutive days',
                'icon': '📚',
                'experience_award': 750,
            },
            {
                'name': 'Ultimate Champion',
                'description': 'Reach level 50 and complete all adventures',
                'icon': '🏅',
                'experience_award': 1000,
            },
            {
                'name': 'Word Master',
                'description': 'Learn 200 words',
                'icon': '📖',
                'experience_award': 200,
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
