from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.template import loader
from django.contrib import messages
import random
import json
import datetime
import re
from . import models
from django.db.models import Sum
from os import listdir
from os.path import join
from .forms import SettingsForm

OPTIONS = ["count10", "subtr10", "equation10", "multiplication"]

FIELD_NAMES = ['count10_correct', 'count10_incorrect',
                       'subtr10_correct', 'subtr10_incorrect',
                       'equation10_correct', 'equation10_incorrect',
                       'multiplication_correct', 'multiplication_incorrect']

SOSTAV_4ISLA = sostav_4isla = [(1,9,10), (2,8,10), (3,7,10), (4,6,10), (5,5,10), (6,4,10), (7,3,10), (8,2,10), (9,1,10), (1,8,9), (2,7,9), (3,6,9), (4,5,9), (5,4,9), (6,3,9), (7,2,9), (8,1,9), (1,7,8), (2,6,8), (3,5,8), (4,4,8), (5,3,8), (6,2,8), (7,1,8), (1,6,7), (2,5,7), (3,4,7), (4,3,7), (5,2,7), (6,1,7), (1,5,6), (2,4,6), (3,3,6), (4,2,6), (5,1,6), (1,4,5), (2,3,5), (3,2,5), (4,1,5), (1,3,4), (2,2,4), (3,1,4), (1,2,3), (2,1,3), (1,1,2),]


def index(request):


    return render(request, 'index.html')


def settings(request):
    # returns from rendered settings page with user settings
    # and creates new row in db (new session row)
    # then checks what types of exercises have been chosen by a user (ifs)
    # and marks according fields in db by a 0
    if request.method == 'POST':
        test_form = SettingsForm(request.POST)

        if test_form.is_valid():
            session_date = datetime.datetime.now()
            total = test_form.cleaned_data['total']

            new_session_row = models.MathStatistics(session_date=session_date, total=total)

            for chosen_option in test_form.cleaned_data['primery_eto_ya']:
                new_session_row[f'{chosen_option}_correct'] = 0
                new_session_row[f'{chosen_option}_incorrect'] = 0

            new_session_row.save()
            return redirect('solving')
        else:
            return render(request, 'settings_page.html', {'test_form': test_form})
    else:
        # at first run renders settings page
        test_form = SettingsForm()
        return render(request, 'settings_page.html', {'test_form': test_form})

def solving(request):
    def count10():
        tuple_ready = random.choice(SOSTAV_4ISLA)
        tuple_with_sym = {"value1": tuple_ready[0], "sign1": "+", "value2": tuple_ready[1],
                          "sign2": '=', "result": tuple_ready[2]}
        return tuple_with_sym

    def subtr10():
        tuple_ready = random.choice(SOSTAV_4ISLA)
        tuple_with_sym = {"value1": tuple_ready[2], "sign1": "-", "value2": tuple_ready[1],
                          "sign2": '=', "result": tuple_ready[0]}
        return tuple_with_sym

    def equation10():
        # randomly chooses what type
        random_type = random.choice([count10, subtr10])
        # runs according function
        basic_primer = random_type()
        #creates 2 variants of exercise, with input in different positions
        tuple_with_sym1 = {"result": basic_primer['value1'], "sign1": basic_primer['sign1'], "value1": basic_primer['value2'], "sign2": '=', "value2": basic_primer['result']}
        tuple_with_sym2 = {"value1": basic_primer['value1'], "sign1": basic_primer['sign1'], "result": basic_primer['value2'], "sign2": '=', "value2": basic_primer['result']}
        return random.choice([tuple_with_sym1, tuple_with_sym2])

    def multiplication():
        multiplication_table = []
        pass

    # variable to count how many exercises have been passed
    exercises_counter = 0

    # checks in db what types have been chosen and adds them to 'chosen settings'
    chosen_settings = []
    for field_name in FIELD_NAMES:
        if eval(f'models.MathStatistics.objects.last().{field_name}') != None:
            exercises_counter += eval(f'models.MathStatistics.objects.last().{field_name}')
            func = re.split("_", field_name)[0]
            chosen_settings.append(func)
    # if passed exercises < goal exercises creates random exercise and renders page with this exercsise
    if exercises_counter < models.MathStatistics.objects.last().total:
        random_primer = random.choice(chosen_settings)
        primer = eval(f'{random_primer}{()}')
        json_primer = json.dumps(primer)

        return render(request, 'solving.html', {'ready_primer': json.loads(json_primer), 'primer_type': random_primer})
    else:
        return redirect('session_results')

def register_solution(request, primer_type, result):
    primer_type_for_db = f"{primer_type}_{result}"
    last_record = models.MathStatistics.objects.last()
    last_records_value = int(getattr(models.MathStatistics.objects.last(), primer_type_for_db))
    new_record = setattr(last_record, primer_type_for_db, last_records_value+1)
    last_record.save()
    return redirect('solving')


def session_results(request):
    correct_answers = 0
    incorrect_answers = 0
    total_questions = int(getattr(models.MathStatistics.objects.last(), 'total'))
    for field_name in FIELD_NAMES:
        item = getattr(models.MathStatistics.objects.last(), field_name)
        if item != None:
            if re.findall('_correct$', field_name):
                correct_answers += item
            else:
                incorrect_answers += item

    index_image_list = listdir("mathapp/static/images")
    index_image_list.remove("Thumbs.db")
    index_image = random.choice(index_image_list)


    return render(request, 'session_results.html', {'total': total_questions, 'correct_answers': correct_answers,
                                                    'incorrect_answers': incorrect_answers, 'index_image': f"/images/{index_image}"})

def statistics(request):
    exercises_total = 0
    exercises_correct_total = 0
    exercises_incorrect_total = 0
    ready_dict = {}

    for field in FIELD_NAMES:
        questions_number = models.MathStatistics.objects.aggregate(Sum(field))
        for key, value in questions_number.items():
            if value != None:
                ready_dict[field] = value
                if re.findall('_correct$', field):
                    exercises_correct_total += value
                else:
                    exercises_incorrect_total += value

    ready_dict['total_correct'] = exercises_correct_total
    ready_dict['total_incorrect'] = exercises_incorrect_total

    return render(request, 'statistics.html', ready_dict)