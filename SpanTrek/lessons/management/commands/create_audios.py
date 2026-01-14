#!/usr/bin/env python3

import json
from django.core.management.base import BaseCommand
from gtts import gTTS
import os
import re
from lessons.models import Audio, Vocabulary, Sentence

def normalize_filename(text):
    """
    Convert Spanish characters to English equivalents for filenames
    """
    # Dictionary mapping Spanish characters to English equivalents
    spanish_to_english = {
        'á': 'a', 'à': 'a', 'ä': 'a', 'â': 'a',
        'é': 'e', 'è': 'e', 'ë': 'e', 'ê': 'e',
        'í': 'i', 'ì': 'i', 'ï': 'i', 'î': 'i',
        'ó': 'o', 'ò': 'o', 'ö': 'o', 'ô': 'o',
        'ú': 'u', 'ù': 'u', 'ü': 'u', 'û': 'u',
        'ñ': 'n',
        'ç': 'c',
        # Uppercase versions
        'Á': 'A', 'À': 'A', 'Ä': 'A', 'Â': 'A',
        'É': 'E', 'È': 'E', 'Ë': 'E', 'Ê': 'E',
        'Í': 'I', 'Ì': 'I', 'Ï': 'I', 'Î': 'I',
        'Ó': 'O', 'Ò': 'O', 'Ö': 'O', 'Ô': 'O',
        'Ú': 'U', 'Ù': 'U', 'Ü': 'U', 'Û': 'U',
        'Ñ': 'N',
        'Ç': 'C'
    }
    
    # Replace Spanish characters with English equivalents
    normalized = text
    for spanish_char, english_char in spanish_to_english.items():
        normalized = normalized.replace(spanish_char, english_char)
    
    # Replace spaces with underscores and remove special characters
    # Remove special chars except spaces and hyphens
    normalized = re.sub(r'[^\w\s-]', '', normalized)  
    # Replace spaces and hyphens with underscores
    normalized = re.sub(r'[\s-]+', '_', normalized)   
    # Convert to lowercase
    normalized = normalized.lower()                    
    
    # Remove Spanish articles from the beginning
    articles = ['el_', 'la_', 'los_', 'las_', 'un_', 'una_', 'unos_', 'unas_']
    for article in articles:
        if normalized.startswith(article):
            normalized = normalized[len(article):]
            break
     
    # If the filename is a Windows reserved name, add prefix
    if normalized == 'con':
        normalized = f'word_{normalized}'
    
    return normalized

def create_audio_file(text, audio_type):
    """
    Create an MP3 file from text using GTTS - Google Text-to-Speech
    """
    # Create the TTS object
    tts = gTTS(text=text, lang='es', slow=False)
    
    # Normalize the filename to remove Spanish characters
    normalized_filename = normalize_filename(text)
    
    output_path = os.path.join('static', 'audio', audio_type, f'{normalized_filename}.mp3')
    
    tts.save(output_path)
    print(f"Audio file created: {output_path}")

class Command(BaseCommand):
    help = 'Creates MP3 audio files from audios.json file'
    
    # Add argument determining source of audio text
    def add_arguments(self, parser):
        # --audio-from sentences/vocabulary
        parser.add_argument(
            '--audio-from',
            type=str,
            help='Text to convert to speech (optional, overrides JSON file)'
        ) 
    
    def handle(self, *args, **options):
        audio_from = options.get('audio_from')
        
        if not audio_from or audio_from not in ['vocabulary', 'sentences']:
            self.stdout.write(self.style.ERROR('Please specify --audio-from with either "vocabulary" or "sentences"'))
            return
    
        try:
            # Get data from database
            if audio_from == 'vocabulary':
                items = Vocabulary.objects.all()
                self.stdout.write(self.style.SUCCESS(f'Found {items.count()} vocabulary items in database'))
            elif audio_from == 'sentences':
                items = Sentence.objects.all()
                self.stdout.write(self.style.SUCCESS(f'Found {items.count()} sentence items in database'))
            
            created_count = 0
            skipped_count = 0
            
            for item in items:
                # Get the text based on audio_from type
                if audio_from == 'vocabulary':
                    text = item.word
                elif audio_from == 'sentences':
                    text = item.sentence
                
                # Create or get audio object (using audio_url as unique key to avoid duplicates)
                audio_url = f'/static/audio/{audio_from}/{normalize_filename(text)}.mp3'
                audio, created = Audio.objects.get_or_create(
                    audio_url=audio_url,
                    defaults={'text': text}
                )
                
                if created:
                    created_count += 1
                else:
                    skipped_count += 1
                
                if not os.path.exists(os.path.join('static', 'audio', audio_from, f'{normalize_filename(text)}.mp3')):
                    create_audio_file(text, audio_from)
            
            self.stdout.write(self.style.SUCCESS(
                f'Audio processing complete: {created_count} created, {skipped_count} already existed'
            ))
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error processing audio data: {str(e)}')
            )
            raise
