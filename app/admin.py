from django.contrib import admin
from app.models import Dog, Tag, DogTag, UserSelection
# Register your models here.

admin.site.register(Dog)
admin.site.register(Tag)
admin.site.register(DogTag)
admin.site.register(UserSelection)

