from django.shortcuts import render
from . import models
from random import randint
from django.http import JsonResponse
from django.db.models import Count
import requests
import json

# Create your views here.
def index(request):
    context = {}
    context['question_obj'] = {}
    # size
    context['question_obj']['size'] = {}
    context['question_obj']['size']['question_no'] = 1
    context['question_obj']['size']['question_attr'] = 'size'
    context['question_obj']['size']['question_text'] = 'Which size of dog do you prefer?'
    context['question_obj']['size']['img_urls'] = {}
    context['question_obj']['size']['img_urls']['small_off'] = '/img/size-of-dog-btns/sml-btn.png'
    context['question_obj']['size']['img_urls']['small_on'] = '/img/size-of-dog-btns/sml-btn-down.png'
    context['question_obj']['size']['img_urls']['medium_off'] = '/img/size-of-dog-btns/med-btn.png'
    context['question_obj']['size']['img_urls']['medium_on'] = '/img/size-of-dog-btns/med-btn-down.png'
    context['question_obj']['size']['img_urls']['large_off'] = '/img/size-of-dog-btns/lrg-btn.png'
    context['question_obj']['size']['img_urls']['large_on'] = '/img/size-of-dog-btns/lrg-btn-down.png'
    context['question_obj']['size']['img_urls']['giant_off'] = '/img/size-of-dog-btns/gnt-btn.png'
    context['question_obj']['size']['img_urls']['giant_on'] = '/img/size-of-dog-btns/gnt-btn-down.png'
    # locality
    context['question_obj']['locality'] = {}
    context['question_obj']['locality']['question_no'] = 2
    context['question_obj']['locality']['question_attr'] = 'locality'
    context['question_obj']['locality']['question_text'] = 'Where do you live?'
    context['question_obj']['locality']['img_urls'] = {}
    context['question_obj']['locality']['img_urls']['city_off'] = '/img/living-btns/city-btn.png'
    context['question_obj']['locality']['img_urls']['city_on'] = '/img/living-btns/city-btn-down.png'
    context['question_obj']['locality']['img_urls']['country_off'] = '/img/living-btns/country-btn.png'
    context['question_obj']['locality']['img_urls']['country_on'] = '/img/living-btns/country-btn-down.png'
    # allergies
    context['question_obj']['allergy'] = {}
    context['question_obj']['allergy']['question_no'] = 3
    context['question_obj']['allergy']['question_attr'] = 'allergy'
    context['question_obj']['allergy']['question_text'] = 'Allergies?'
    context['question_obj']['allergy']['img_urls'] = {}
    context['question_obj']['allergy']['img_urls']['yes_allergy_off'] = '/img/allergy-btns/yes-allergy-btn.png'
    context['question_obj']['allergy']['img_urls']['yes_allergy_on'] = '/img/allergy-btns/yes-allergy-btn-down.png'
    context['question_obj']['allergy']['img_urls']['no_allergy_off'] = '/img/allergy-btns/no-allergy-btn.png'
    context['question_obj']['allergy']['img_urls']['no_allergy_on'] = '/img/allergy-btns/no-allergy-btn-down.png'
    # exercise
    context['question_obj']['exercise'] = {}
    context['question_obj']['exercise']['question_no'] = 4
    context['question_obj']['exercise']['question_attr'] = 'exercise'
    context['question_obj']['exercise']['question_text'] = 'Exercise?'
    context['question_obj']['exercise']['img_urls'] = {}
    context['question_obj']['exercise']['img_urls']['short_off'] = '/img/exercise-btns/short-exercise-btn.png'
    context['question_obj']['exercise']['img_urls']['short_on'] = '/img/exercise-btns/short-exercise-btn-down.png'
    context['question_obj']['exercise']['img_urls']['medium_off'] = '/img/exercise-btns/med-exercise-btn.png'
    context['question_obj']['exercise']['img_urls']['medium_on'] = '/img/exercise-btns/med-exercise-btn-down.png'
    context['question_obj']['exercise']['img_urls']['long_off'] = '/img/exercise-btns/long-exercise-btn.png'
    context['question_obj']['exercise']['img_urls']['long_on'] = '/img/exercise-btns/long-exercise-btn-down.png'
    context['question_obj']['exercise']['img_urls']['vlong_off'] = '/img/exercise-btns/vlong-exercise-btn.png'
    context['question_obj']['exercise']['img_urls']['vlong_on'] = '/img/exercise-btns/vlong-exercise-btn-down.png'
    # haircare
    context['question_obj']['haircare'] = {}
    context['question_obj']['haircare']['question_no'] = 5
    context['question_obj']['haircare']['question_attr'] = 'haircare'
    context['question_obj']['haircare']['question_text'] = 'Grooming?'

    return render(request, 'app/index.html', context)

def get_dogs(request):
    context = {}
    #get no list from request
    size_small = int(request.GET['size[small]'])
    size_medium = int(request.GET['size[medium]'])
    size_large = int(request.GET['size[large]'])
    size_giant = int(request.GET['size[giant]'])

    locality_city = int(request.GET['locality[city]'])
    locality_country = int(request.GET['locality[country]'])

    allergy_yes = int(request.GET['allergy[yes]'])
    allergy_no = int(request.GET['allergy[no]'])

    exercise_short = int(request.GET['exercise[short]'])
    exercise_medium = int(request.GET['exercise[medium]'])
    exercise_long = int(request.GET['exercise[long]'])
    exercise_vlong = int(request.GET['exercise[vlong]'])

    haircare_low = int(request.GET['haircare[low]'])
    haircare_high = int(request.GET['haircare[high]'])

    all_dogs = models.Dog.objects.all()

    size_dogs = all_dogs
    # filter for size
    if (size_small == 0):
        size_dogs = size_dogs.exclude(size='Small')
    if (size_medium == 0):
        size_dogs = size_dogs.exclude(size='Medium')
    if (size_large == 0):
        size_dogs = size_dogs.exclude(size='Large')
    if (size_giant == 0):
        size_dogs = size_dogs.exclude(size='Giant')

    # filter for locality
    locality_dogs = size_dogs
    if (locality_city == 1):
        locality_dogs = locality_dogs.exclude(locality='Country')
    if (locality_country == 1):
        locality_dogs = locality_dogs

    # filter for allergies
    allergy_dogs = locality_dogs
    if (allergy_yes == 1):
        allergy_dogs = allergy_dogs.filter(good_for_allergies='Good')

    # filter for exercise
    exercise_dogs = allergy_dogs
    if (exercise_short == 0):
        exercise_dogs = exercise_dogs.exclude(exercise='Up to 30 mins')
    if (exercise_medium == 0):
        exercise_dogs = exercise_dogs.exclude(exercise='Up to 1 hour')
    if (exercise_long == 0):
        exercise_dogs = exercise_dogs.exclude(exercise='Up to 2 hours')
    if (exercise_vlong == 0):
        exercise_dogs = exercise_dogs.exclude(exercise='More than 2 hours')

    # filter for haircare
    haircare_dogs = exercise_dogs
    if (haircare_low == 1 or haircare_high == 0):
        haircare_dogs = haircare_dogs.exclude(grooming='Every day')

    result_dogs = haircare_dogs

    context['dogs'] = []
    for dog in result_dogs:
        c = {}
        c['dog_id'] = str(dog.id)
        c['dog_name'] = str(dog.dog_name)
        c['size'] = str(dog.size)
        c['locality'] = str(dog.locality)
        c['allergies'] = str(dog.good_for_allergies)
        c['exercise'] = str(dog.exercise)
        c['haircare'] = str(dog.grooming)
        context['dogs'].append(c)
    return JsonResponse(context)


# Record selection
def record_selection(request):
    req = request.GET.get
    yes_string_list = req('yes_list').split(',')
    yes_string_list = models.Tag.objects.filter(id__in=yes_string_list)
    yes_string_list = [str(i) for i in yes_string_list]
    yes_string = ','.join(yes_string_list) 
    no_string_list = req('no_list').split(',')
    no_string_list = models.Tag.objects.filter(id__in=no_string_list)
    no_string_list = [str(i) for i in no_string_list]
    no_string = ','.join(no_string_list)
    decision = True if req('outcome') == '1' else False
    selection = models.UserSelection.objects.create(outcome=decision,suggested_dog_id=req('dog'),lat=req('lat'),lng=req('lng'),yes_list=yes_string,no_list=no_string)
    return JsonResponse({'status':'OK'})

# Database amend view
def database(request):
    context = {}
    context['tags'] = models.Tag.objects.all()
    context['activities'] = models.Activity.objects.all()
    return render(request,'database.html',context)
