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
    # Get all known tags
    # Select 5 for questions
    all_tags = list(models.Tag.objects.all())
    # Select 5 for questions
    rand_selection = []
    for i in range(0,5):
        rand_selection.append(randint(0,len(all_tags)-1))
    context['question_tags'] = []
    context['image_url'] = {}
    for i in range(0,5):
        context['question_tags'].append(all_tags[rand_selection[i]])
        tags = [str(all_tags[rand_selection[i]].tag_search_terms)]
        tag_string = ','.join(tags)
        payload = {'api_key': '63c1470d6730c8c27c06176060489644','tags':tag_string,'tag_mode':'any','media':'photos','format':'json','method':'flickr.photos.search'}
        res = requests.get('https://api.flickr.com/services/rest/?',params=payload)
        photo = res.text
        photo = photo[photo.index('{'):len(photo)-1]
        photo = json.loads(photo)
        photo = photo["photos"]["photo"][randint(0,len(photo["photos"]["photo"])-1)]
        farm_id = str(photo["farm"])
        server_id = str(photo["server"])
        id = str(photo["id"])
        secret = str(photo["secret"])
        image_url = "https://farm" + farm_id + ".staticflickr.com/" + server_id + "/" + id + "_" + secret + ".jpg"
        context["image_url"][str(all_tags[rand_selection[i]].id)] = image_url 
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
