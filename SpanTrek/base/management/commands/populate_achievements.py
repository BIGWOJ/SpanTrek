from django.core.management.base import BaseCommand
from base.models import Achievement

class Command(BaseCommand):
    help = 'Populate the database with sample achievements'

    def handle(self, *args, **options):
        achievements_data = [
            # Experience-based achievements
            {
                'name': 'First Steps',
                'description': 'Earn your first experience point',
                'icon': '👶',
                'condition_type': 'experience',
                'condition_value': 1,
                'points_reward': 10,
                'rarity': 'common',
            },
            {
                'name': 'Novice Explorer',
                'description': 'Earn 100 experience points',
                'icon': '🎒',
                'condition_type': 'experience',
                'condition_value': 100,
                'points_reward': 25,
                'rarity': 'common',
            },
            {
                'name': 'Experienced Traveler',
                'description': 'Earn 500 experience points',
                'icon': '🗺️',
                'condition_type': 'experience',
                'condition_value': 500,
                'points_reward': 50,
                'rarity': 'rare',
            },
            {
                'name': 'Master Explorer',
                'description': 'Earn 1000 experience points',
                'icon': '🏔️',
                'condition_type': 'experience',
                'condition_value': 1000,
                'points_reward': 100,
                'rarity': 'epic',
            },
            {
                'name': 'Legendary Adventurer',
                'description': 'Earn 2500 experience points',
                'icon': '👑',
                'condition_type': 'experience',
                'condition_value': 2500,
                'points_reward': 250,
                'rarity': 'legendary',
            },
            
            # Level-based achievements
            {
                'name': 'Level Up!',
                'description': 'Reach level 2',
                'icon': '⬆️',
                'condition_type': 'level',
                'condition_value': 2,
                'points_reward': 20,
                'rarity': 'common',
            },
            {
                'name': 'Rising Star',
                'description': 'Reach level 5',
                'icon': '⭐',
                'condition_type': 'level',
                'condition_value': 5,
                'points_reward': 50,
                'rarity': 'common',
            },
            {
                'name': 'Skilled Learner',
                'description': 'Reach level 10',
                'icon': '🎓',
                'condition_type': 'level',
                'condition_value': 10,
                'points_reward': 100,
                'rarity': 'rare',
            },
            {
                'name': 'Expert Level',
                'description': 'Reach level 20',
                'icon': '🏆',
                'condition_type': 'level',
                'condition_value': 20,
                'points_reward': 200,
                'rarity': 'epic',
            },
            
            # Streak-based achievements
            {
                'name': 'Getting Started',
                'description': 'Complete 3 days in a row',
                'icon': '🔥',
                'condition_type': 'streak',
                'condition_value': 3,
                'points_reward': 30,
                'rarity': 'common',
            },
            {
                'name': 'Week Warrior',
                'description': 'Complete 7 days in a row',
                'icon': '📅',
                'condition_type': 'streak',
                'condition_value': 7,
                'points_reward': 70,
                'rarity': 'common',
            },
            {
                'name': 'Streak Master',
                'description': 'Complete 14 days in a row',
                'icon': '💪',
                'condition_type': 'streak',
                'condition_value': 14,
                'points_reward': 140,
                'rarity': 'rare',
            },
            {
                'name': 'Unstoppable',
                'description': 'Complete 30 days in a row',
                'icon': '🚀',
                'condition_type': 'streak',
                'condition_value': 30,
                'points_reward': 300,
                'rarity': 'epic',
            },
            {
                'name': 'Dedication Master',
                'description': 'Complete 100 days in a row',
                'icon': '💎',
                'condition_type': 'streak',
                'condition_value': 100,
                'points_reward': 1000,
                'rarity': 'legendary',
            },
            
            # Adventure progress achievements
            {
                'name': 'Journey Begins',
                'description': 'Make progress in your first adventure',
                'icon': '🌟',
                'condition_type': 'adventure_progress',
                'condition_value': 1,
                'points_reward': 15,
                'rarity': 'common',
            },
            {
                'name': 'Adventure Seeker',
                'description': 'Complete 50% of adventures',
                'icon': '🗝️',
                'condition_type': 'adventure_progress',
                'condition_value': 50,
                'points_reward': 75,
                'rarity': 'rare',
            },
            {
                'name': 'Quest Master',
                'description': 'Complete all adventures',
                'icon': '🏰',
                'condition_type': 'adventure_progress',
                'condition_value': 100,
                'points_reward': 500,
                'rarity': 'legendary',
            },
            
            # Custom achievements
            {
                'name': 'Well Rounded',
                'description': 'Reach level 3 with a 5+ day streak',
                'icon': '⚖️',
                'condition_type': 'custom',
                'condition_value': 0,  # Not used for custom
                'points_reward': 100,
                'rarity': 'rare',
            },
            {
                'name': 'Perfectionist',
                'description': 'Have your level equal your streak (min 10)',
                'icon': '🎯',
                'condition_type': 'custom',
                'condition_value': 0,  # Not used for custom
                'points_reward': 200,
                'rarity': 'epic',
                'is_hidden': True,  # Hidden achievement
            },
            {
                'name': 'Spanish Champion',
                'description': 'Complete the ultimate Spanish challenge',
                'icon': '🇪🇸',
                'condition_type': 'experience',
                'condition_value': 5000,
                'points_reward': 500,
                'rarity': 'legendary',
                'is_hidden': True,
            },
        ]

        created_count = 0
        updated_count = 0

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
                # Update existing achievement with new data
                for key, value in achievement_data.items():
                    if key != 'name':  # Don't update the name (it's the lookup key)
                        setattr(achievement, key, value)
                achievement.save()
                updated_count += 1
                self.stdout.write(
                    self.style.WARNING(f'Updated achievement: {achievement.name}')
                )

        self.stdout.write(
            self.style.SUCCESS(
                f'\nCompleted! Created {created_count} new achievements, updated {updated_count} existing ones.'
            )
        )
