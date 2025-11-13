from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from lessons.models import Vocabulary, Sentence, Audio
import random


@login_required
def practice_intro(request, practice_type):
    # Get default count using dynamic attribute access
    default_count_attr = f'default_{practice_type}_practice_count'
    question_count = getattr(request.user, default_count_attr)
    question_count = request.POST.get('question_count', question_count)
    
    request.session['question_count'] = question_count  

    practice_set = []
    learned_words = request.user.words_learned or []
    learned_sentences = request.user.sentences_learned or []
    learned_audios = request.user.audio_learned or []
    all_vocabularies = Vocabulary.objects.filter(word__in=learned_words).distinct()
    all_sentences = Sentence.objects.filter(sentence__in=learned_sentences).distinct()
    all_audios = Audio.objects.filter(text__in=learned_audios).distinct()
    match practice_type:
        case 'random':
            practice_set = random.sample(
                list(all_vocabularies) + list(all_sentences) + list(all_audios), 
                k=min(int(question_count), len(all_vocabularies) + len(all_sentences) + len(all_audios))
            ) 
        case 'vocabulary':
            entire_set = all_vocabularies
        case 'sentence':
            entire_set = all_sentences
        case 'listening':
            entire_set = all_audios

    practice_set = practice_set or random.sample(list(entire_set), k=min(int(question_count), len(entire_set)))
    print('l',learned_audios)
    print('all_audios', all_audios)
    print('entire_set', entire_set)
    print(request.user.audio_learned)
    print(practice_set)
    if request.method == 'POST':
        # Store practice type and practice set in session for navigation
        request.session['practice_type'] = practice_type
        practice_items = []
        for item in practice_set:
            item_data = {
                'type': item.__class__.__name__.lower(),
            }
            if hasattr(item, 'word'):  # Vocabulary
                item_data.update({
                    'word': item.word,
                    'translation': item.translation,
                })
            elif hasattr(item, 'sentence'):  # Sentence
                item_data.update({
                    'sentence': item.sentence,
                    'translation': item.translation,
                })
            elif hasattr(item, 'audio_url'):  # Audio
                item_data.update({
                    'audio_url': item.audio_url,
                    'text': item.text,
                })
            practice_items.append(item_data)
        
        request.session['practice_items'] = practice_items
        return redirect('practice:practice_main', index=0)

    context = {
        'practice_type': practice_type,
        'question_count': question_count
    }

    return render(request, 'practice/intro.html', context=context)

@login_required
def practice_main(request, index):
    practice_items = request.session.get('practice_items', [])
    
    if not practice_items or index >= len(practice_items):
        return redirect('practice:practice_intro', practice_type='vocabulary')
    
    current_exercise = practice_items[index]
    current_exercise = [current_exercise['type'], (current_exercise.get('word') or current_exercise.get('sentence') or current_exercise.get('audio_url')), (current_exercise.get('translation') or current_exercise.get('text'))]
    
    if current_exercise[0] == 'audio': 
        current_exercise.append('Write what you hear')
        current_exercise[2], current_exercise[3] = current_exercise[3], current_exercise[2]
    
    total_count = len(practice_items)
    current_number = index + 1

    # Check if there's a next item
    has_next = index + 1 < total_count
    next_index = index + 1 if has_next else None

    context = {
        'current_exercise': current_exercise,
        'current_number': current_number,
        'total_count': total_count,
        'has_next': has_next,
        'next_index': next_index,
        'is_end': not has_next,
    }
    
    return render(request, 'practice/practice_main.html', context=context)

@login_required
def practice_complete(request):
    
    practice_items = request.session.get('practice_items', [])
    
    if not practice_items:
        return redirect('practice:practice_intro', practice_type='vocabulary')
    
    # Determine practice type from the session or default to 'vocabulary'
    practice_type = request.session.get('practice_type', 'vocabulary')
    total_count = len(practice_items)
    
    request.user.update_progress_after_practice(practice_type=practice_type)
    request.user.progress_daily_challenges(practice_type=practice_type)

    context = {
        'practice_type': practice_type,
        'total_count': total_count,
    }
    
    return render(request, 'practice/practice_complete.html', context=context)

