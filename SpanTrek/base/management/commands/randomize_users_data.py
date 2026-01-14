from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from lessons.models import Lesson, Country
import random
from datetime import date, timedelta
from base.services import AchievementService
from django.db.models import Case, When, Value, IntegerField

class Command(BaseCommand):
    help = 'Randomizes user data to simulate different progress levels'

    def handle(self, *args, **options):
        User = get_user_model()
        
        # Get all users except superuser
        users = User.objects.filter(is_superuser=False)
        
        if not users.exists():
            self.stdout.write(self.style.WARNING('No users found to randomize'))
            return
        
        # Get lesson data from database
        poland_obj = Country.objects.filter(name='poland').first()
        if not poland_obj:
            self.stdout.write(self.style.ERROR('Poland country not found in database'))
            return

        updated_count = 0
        updated_count_0_progress = 0
        for user in users:
            try:                                                
                # Random adventure progress
                adventure_progress = random.randint(0, 9)
                
                # Only if adventure progress is not zero, randomize data (not possible to get experience without lessons)
                if adventure_progress == 0:
                    updated_count_0_progress += 1
                    continue
                
                user.adventure_progress = adventure_progress
                
                # Random level and experience
                # 50*500 => experience for level 50 max
                user.experience = random.randint(0, 50*500)
                user.level = user.experience // 500 + 1
                    
                # Random streak data
                user.days_streak = random.randint(0, 15)
                user.highest_streak = random.randint(user.days_streak, 30)
                
                # Random activity days (last 30 days)
                user.activity_days = []
                today = date.today()
                for i in range(30):
                    activity_date = today - timedelta(days=i)
                    # 40% chance of activity each day
                    if random.random() < 0.4:  
                        user.activity_days.append(activity_date.isoformat())
                
                if user.activity_days:
                    user.last_activity_date = max([date.fromisoformat(d) for d in user.activity_days])
                    
                
                # Calculate progress for each landmark in order
                landmarks_progress = {}
                remaining_progress = adventure_progress
                
                for landmark in ['szczecin', 'poznan', 'warsaw']:
                    landmark_lessons = min(3, remaining_progress)
                    if landmark_lessons > 0:
                        landmarks_progress[landmark] = landmark_lessons
                    remaining_progress = max(0, remaining_progress - 3)
                
                user.landmark_lessons_progress = landmarks_progress
                
                # Country progress (Poland only, max 9 lessons total)
                poland_progress = adventure_progress
                user.country_lessons_progress = {'poland': poland_progress} if poland_progress > 0 else {}
                
                # Knowledge based on completed lessons
                user.words_learned = []
                user.sentences_learned = []
                user.audio_learned = []
                user.use_of_spanish = 0
                if adventure_progress > 0:
                    # Get all lessons in specific order: szczecin, poznan, warsaw to properly get knowledge
                    all_lessons_in_order = Lesson.objects.filter(country=poland_obj).order_by(
                        Case(
                            When(landmark__name='szczecin', then=Value(1)),
                            When(landmark__name='poznan', then=Value(2)),
                            When(landmark__name='warsaw', then=Value(3)),
                            output_field=IntegerField(),
                        ),
                        'order'
                    )

                    for lesson in all_lessons_in_order[:poland_progress]:
                        # Words
                        lesson_words = set(vocab.word for vocab in lesson.vocabularies.all())
                        if not isinstance(user.words_learned, list):
                            user.words_learned = []
                        new_words = lesson_words - set(user.words_learned)
                        user.words_learned.extend(new_words)
                        
                        # Sentences
                        lesson_sentences = set(sentence.sentence for sentence in lesson.sentences.all()) 
                        if not isinstance(user.sentences_learned, list):
                            user.sentences_learned = []
                        new_sentences = lesson_sentences - set(user.sentences_learned)
                        user.sentences_learned.extend(new_sentences)

                        # Audio
                        lesson_audios = set(audio.text for audio in lesson.audios.all())
                        if not isinstance(user.audio_learned, list):
                            user.audio_learned = []
                        new_audios = lesson_audios - set(user.audio_learned)
                        user.audio_learned.extend(new_audios)
                        
                        # Use of Spanish
                        user.use_of_spanish += lesson.use_of_spanish
                
                # Random daily challenges
                user.create_daily_challenges()
                
                # Random passports (countries completed -> only Poland for now)
                user.passports_earned = ['poland'] if poland_progress >= 9 else []
                
                # Random avatar from 15 available
                user.avatar = f'avatars/{random.randint(1, 15)}.png'
                
                # Save user first before setting achievements
                user.save()
                
                # Check and award achievements
                AchievementService.clear_achievements(user)
                AchievementService.check_and_award_achievements(user)
                
                updated_count += 1
                
                self.stdout.write(
                    self.style.SUCCESS(f'Randomized user: {user.username}')
                )
                
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'Error randomizing user {user.username}: {str(e)}')
                )
        
        # Summary
        self.stdout.write('\n' + '='*50)
        self.stdout.write(f'User data randomization summary:')
        self.stdout.write(self.style.SUCCESS(f'Updated: {updated_count} users'))
        self.stdout.write(self.style.SUCCESS(f'Updated with 0 adventure progress: {updated_count_0_progress} users'))
        self.stdout.write('='*50)