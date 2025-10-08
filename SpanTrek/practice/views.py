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
    match practice_type:
        case 'random':
            all_vocabularies = Vocabulary.objects.all()
            all_sentences = Sentence.objects.all()
            all_audios = Audio.objects.all()
            practice_set = random.sample(
                list(all_vocabularies) + list(all_sentences) + list(all_audios), 
                k=min(int(question_count), len(all_vocabularies) + len(all_sentences) + len(all_audios))
            ) 
        case 'vocabulary':
            entire_set = Vocabulary.objects.all()
        case 'sentence':
            entire_set = Sentence.objects.all()
        case 'listening':
            entire_set = Audio.objects.all()

    practice_set = practice_set or random.sample(list(entire_set), k=min(int(question_count), len(entire_set)))

    if request.method == 'POST':
        return practice_main(request, practice_set)

    context = {
        'practice_type': practice_type,
        'question_count': question_count
    }

    return render(request, 'practice/intro.html', context=context)

def practice_main(request, practice_set):
    question_count = request.session.get('question_count')

    context = {
        'question_count': question_count,
        'practice_set': practice_set
    }
    
    return render(request, 'practice/practice_main.html', context=context)

