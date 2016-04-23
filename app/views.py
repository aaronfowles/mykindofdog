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
    context['question_obj']['size']['img_urls']['small_off'] = '/img/size-of-dog-btns/sml-btn.svg'
    context['question_obj']['size']['img_urls']['small_on'] = '/img/size-of-dog-btns/sml-btn-down.svg'
    context['question_obj']['size']['img_urls']['medium_off'] = '/img/size-of-dog-btns/med-btn.svg'
    context['question_obj']['size']['img_urls']['medium_on'] = '/img/size-of-dog-btns/med-btn-down.svg'
    context['question_obj']['size']['img_urls']['large_off'] = '/img/size-of-dog-btns/lrg-btn.svg'
    context['question_obj']['size']['img_urls']['large_on'] = '/img/size-of-dog-btns/lrg-btn-down.svg'
    context['question_obj']['size']['img_urls']['giant_off'] = '/img/size-of-dog-btns/gnt-btn.svg'
    context['question_obj']['size']['img_urls']['giant_on'] = '/img/size-of-dog-btns/gnt-btn-down.svg'
    # locality
    context['question_obj']['locality'] = {}
    context['question_obj']['locality']['question_no'] = 2
    context['question_obj']['locality']['question_attr'] = 'locality'
    context['question_obj']['locality']['question_text'] = 'Where do you live?'
    context['question_obj']['locality']['img_urls'] = {}
    context['question_obj']['locality']['img_urls']['city_off'] = ''
    context['question_obj']['locality']['img_urls']['city_on'] = ''
    context['question_obj']['locality']['img_urls']['country_off'] = ''
    context['question_obj']['locality']['img_urls']['country_on'] = ''
    return render(request, 'app/index.html', context)

def get_dogs(request):
    context = {}
    #get no list from request
    response_list = request.GET['size[small]']

    size_small = response_list
    print(response_list)

    all_dogs = models.Dog.objects.all()

    test_dog = all_dogs[0]

    context['dog_id'] = test_dog.id
    context['dog_name'] = test_dog.dog_name
    context['is_small_on'] = size_small
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
