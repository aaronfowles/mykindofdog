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
    context['question_obj']['size']['img_urls']['small_off'] = ''
    context['question_obj']['size']['img_urls']['small_on'] = ''
    context['question_obj']['size']['img_urls']['medium_off'] = ''
    context['question_obj']['size']['img_urls']['medium_on'] = ''
    context['question_obj']['size']['img_urls']['large_off'] = ''
    context['question_obj']['size']['img_urls']['large_on'] = ''
    context['question_obj']['size']['img_urls']['giant_off'] = ''
    context['question_obj']['size']['img_urls']['giant_on'] = ''
    # locality
    context['question_obj']['locality'] = {}
    context['question_obj']['locality']['question_no'] = 2
    context['question_obj']['locality']['question_attr'] = 'locality'
    context['question_obj']['locality']['question_text'] = 'Where do you live?'
    context['question_obj']['size']['img_urls']['city_off'] = ''
    context['question_obj']['size']['img_urls']['city_on'] = ''
    context['question_obj']['size']['img_urls']['country_off'] = ''
    context['question_obj']['size']['img_urls']['country_on'] = ''
    return render(request, 'app/index.html', context)

def get_dogs(request):
    context = {}
    #get no list from request
    no_list = request.GET.get("no_list","")
    yes_list = request.GET.get("yes_list","")

    no_list = no_list.split(',')
    yes_list = yes_list.split(',')
    if no_list[0] == '':
        no_list = [1,2]
    if yes_list[0] == '':
        yes_list = [3,4]

    all_dog_tags = models.DogTag.objects.all()
    dogs_to_exclude = all_dog_tags.filter(tag_id__in=no_list)
    dog_ids_to_exclude = []
    for dog in dogs_to_exclude:
        dog_ids_to_exclude.append(dog.dog_id.id)

    dogs_to_prefer = models.DogTag.objects.filter(tag_id__in=yes_list)
    dog_ids_to_prefer = []
    for dog in dogs_to_prefer:
        dog_ids_to_prefer.append(dog.dog_id.id)

    dog_ids_to_remove = set(dog_ids_to_prefer).intersection(dog_ids_to_exclude)
    dog_ids_to_select = [i for i in dog_ids_to_prefer if i not in dog_ids_to_remove]
    chosen_dog = None
    if (len(dog_ids_to_select) == 0):
        chosen_dog = models.Dog.objects.exclude(id__in=dog_ids_to_exclude)[0]
    elif (len(dog_ids_to_select) == 1):
        chosen_dog = models.Dog.objects.filter(id__in=dog_ids_to_select)[0]
    else:
        a = models.DogTag.objects.filter(dog_id__in=dog_ids_to_select)
        a2 = a.filter(tag_id__in=yes_list)
        b = a2.values('dog_id').annotate(total=Count('dog_id')).order_by('-total')
        chosen_dog = models.Dog.objects.get(id=b[0]['dog_id'])
    if (chosen_dog == None):
        chosen_dog.dog_desc = "Hmmm, iDunno doesn't know..."

    context['dog_id'] = chosen_dog.id
    context['dog_name'] = chosen_dog.dog_name
    context['search_term'] = chosen_dog.search_term
    context['dog_desc'] = chosen_dog.dog_desc
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
