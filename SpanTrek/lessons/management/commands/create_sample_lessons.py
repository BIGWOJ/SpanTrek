from django.core.management.base import BaseCommand
from lessons.models import (
    Lesson, Word, ListeningExercise, ReadingPassage,
    LessonWord, LessonListening, LessonReading
)

class Command(BaseCommand):
    help = 'Create sample lesson data for testing'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample lesson data...')

        # Create sample words
        words_data = [
            {
                'spanish_word': 'hola',
                'english_translation': 'hello',
                'example_sentence_spanish': '¡Hola! ¿Cómo estás?',
                'example_sentence_english': 'Hello! How are you?'
            },
            {
                'spanish_word': 'gracias',
                'english_translation': 'thank you',
                'example_sentence_spanish': 'Gracias por tu ayuda.',
                'example_sentence_english': 'Thank you for your help.'
            },
            {
                'spanish_word': 'casa',
                'english_translation': 'house',
                'example_sentence_spanish': 'Mi casa es pequeña.',
                'example_sentence_english': 'My house is small.'
            },
            {
                'spanish_word': 'agua',
                'english_translation': 'water',
                'example_sentence_spanish': 'Necesito agua fría.',
                'example_sentence_english': 'I need cold water.'
            },
            {
                'spanish_word': 'libro',
                'english_translation': 'book',
                'example_sentence_spanish': 'Este libro es muy interesante.',
                'example_sentence_english': 'This book is very interesting.'
            },
            {
                'spanish_word': 'complicado',
                'english_translation': 'complicated',
                'example_sentence_spanish': 'Este problema es muy complicado.',
                'example_sentence_english': 'This problem is very complicated.'
            },
            {
                'spanish_word': 'desarrollar',
                'english_translation': 'to develop',
                'example_sentence_spanish': 'Quiero desarrollar mis habilidades.',
                'example_sentence_english': 'I want to develop my skills.'
            }
        ]

        words = []
        for word_data in words_data:
            word, created = Word.objects.get_or_create(
                spanish_word=word_data['spanish_word'],
                english_translation=word_data['english_translation'],
                defaults=word_data
            )
            words.append(word)
            if created:
                self.stdout.write(f'Created word: {word.spanish_word}')

        # Create sample reading passages
        reading_data = [
            {
                'title': 'Mi Familia',
                'content': '''Hola, me llamo María. Tengo una familia grande. Mi padre se llama Juan y mi madre se llama Ana. 
                Tengo dos hermanos: Carlos y Luis. Carlos es mayor que yo, tiene 25 años. Luis es menor, tiene solo 15 años. 
                Vivimos en una casa bonita con un jardín pequeño. Nos gusta pasar tiempo juntos los fines de semana.''',
                'word_count': 65
            },
            {
                'title': 'En el Restaurante',
                'content': '''Ayer fui a un restaurante español con mis amigos. El camarero fue muy amable y nos explicó el menú. 
                Pedí paella valenciana, que es mi plato favorito. Mis amigos pidieron tapas variadas y sangría. 
                La comida estaba deliciosa y pasamos una velada muy agradable. Definitivamente volveremos pronto.''',
                'word_count': 55
            }
        ]

        readings = []
        for reading_item in reading_data:
            reading, created = ReadingPassage.objects.get_or_create(
                title=reading_item['title'],
                defaults=reading_item
            )
            readings.append(reading)
            if created:
                self.stdout.write(f'Created reading: {reading.title}')

        # Create sample listening exercises
        listening_data = [
            {
                'title': 'Presentaciones Básicas',
                'description': 'Learn basic introductions in Spanish',
                'transcript': '''Hola, me llamo Pedro. Soy de Madrid, España. 
                Tengo 30 años y soy profesor de español. 
                Me gusta enseñar a estudiantes de todo el mundo.''',
                'duration_seconds': 45
            }
        ]

        listenings = []
        for listening_item in listening_data:
            listening, created = ListeningExercise.objects.get_or_create(
                title=listening_item['title'],
                defaults=listening_item
            )
            listenings.append(listening)
            if created:
                self.stdout.write(f'Created listening: {listening.title}')

        # Create sample lessons
        lessons_data = [
            {
                'title': 'Basic Greetings and Introductions',
                'description': 'Learn essential Spanish greetings and how to introduce yourself',
                'order': 1
            },
            {
                'title': 'Family and Home',
                'description': 'Vocabulary and expressions related to family members and home',
                'order': 2
            },
            {
                'title': 'At the Restaurant',
                'description': 'Learn to order food and interact in Spanish restaurants',
                'order': 3
            }
        ]

        lessons = []
        for lesson_data in lessons_data:
            lesson, created = Lesson.objects.get_or_create(
                title=lesson_data['title'],
                defaults=lesson_data
            )
            lessons.append(lesson)
            if created:
                self.stdout.write(f'Created lesson: {lesson.title}')

        # Associate content with lessons
        if lessons:
            # Lesson 1: Basic greetings
            lesson1 = lessons[0]
            basic_words = words[:3]  # First 3 words
            for i, word in enumerate(basic_words):
                LessonWord.objects.get_or_create(
                    lesson=lesson1,
                    word=word,
                    defaults={'order': i}
                )
            
            if readings:
                LessonReading.objects.get_or_create(
                    lesson=lesson1,
                    reading_passage=readings[0],
                    defaults={'order': 0}
                )
            
            if listenings:
                LessonListening.objects.get_or_create(
                    lesson=lesson1,
                    listening_exercise=listenings[0],
                    defaults={'order': 0}
                )

            # Lesson 2: Family and home
            if len(lessons) > 1:
                lesson2 = lessons[1]
                family_words = [w for w in words if w.spanish_word in ['casa', 'agua', 'libro']]
                for i, word in enumerate(family_words):
                    LessonWord.objects.get_or_create(
                        lesson=lesson2,
                        word=word,
                        defaults={'order': i}
                    )

            # Lesson 3: Restaurant
            if len(lessons) > 2 and len(readings) > 1:
                lesson3 = lessons[2]
                remaining_words = words[3:]  # Remaining words
                for i, word in enumerate(remaining_words):
                    LessonWord.objects.get_or_create(
                        lesson=lesson3,
                        word=word,
                        defaults={'order': i}
                    )
                
                LessonReading.objects.get_or_create(
                    lesson=lesson3,
                    reading_passage=readings[1],
                    defaults={'order': 0}
                )

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created sample data: '
                f'{len(words)} words, {len(readings)} readings, '
                f'{len(listenings)} listening exercises, {len(lessons)} lessons'
            )
        )
