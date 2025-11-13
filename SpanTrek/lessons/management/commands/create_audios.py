#!/usr/bin/env python3

import json
from django.core.management.base import BaseCommand
from gtts import gTTS
import os
import re
from lessons.models import Audio

def normalize_filename(text):
    """
    Convert Spanish characters to English equivalents for filenames
    
    Args:
        text (str): The text to normalize
        
    Returns:
        str: Normalized text suitable for filenames
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
    normalized = re.sub(r'[^\w\s-]', '', normalized)  # Remove special chars except spaces and hyphens
    normalized = re.sub(r'[\s-]+', '_', normalized)   # Replace spaces and hyphens with underscores
    normalized = normalized.lower()                    # Convert to lowercase
    
    return normalized

def create_audio_file(text, audio_type):
    """
    Create an MP3 file from text using GTTS - Google Text-to-Speech
    
    Args:
        text (str): The text to convert to speech
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
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        
        audio_from = options.get('audio_from')
        json_data = ''
        
        json_data = os.path.join(base_dir, 'landmark_data', f'{audio_from}.json')
        
        if not os.path.exists(json_data):
            self.stdout.write(self.style.ERROR('No audios.json data file found'))
            return
    
        try:
            with open(json_data, 'r', encoding='utf-8') as f:
                audio_data = json.load(f)
    
            for data in audio_data:
                if audio_from == 'vocabulary':
                    text = data['word']
                elif audio_from == 'sentences':
                    text = data['sentence']
                
                audio, created = Audio.objects.get_or_create(
                    text=text,
                    audio_url=f'/static/audio/{audio_from}/{normalize_filename(text)}.mp3'
                )
                if created:
                    create_audio_file(text, audio_from)
    
            self.stdout.write(self.style.SUCCESS('Audio files created successfully'))
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error processing audio data: {str(e)}')
            )
            raise
