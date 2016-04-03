from __future__ import unicode_literals

from django.db import models

# Activity. AcivityID,ActivityName,ActivityClass
class Dog(models.Model):
    dog_name = models.CharField(max_length=50)
    search_term = models.CharField(max_length=50)
    dog_desc = models.CharField(max_length=50)

    def __str__(self):
        return self.dog_name 

# Tags. TagID,TagName,QuestionText 
class Tag(models.Model):
    tag_name = models.CharField(max_length=50)
    question_text = models.CharField(max_length=50)

    def __str__(self):
        return self.tag_name

# ActivityTags. ActivityID,TagID
class DogTag(models.Model):
    dog_id = models.ForeignKey(Dog, on_delete=models.CASCADE)
    tag_id = models.ForeignKey(Tag, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.dog_id) + str(self.tag_id)

# User Selections. Outcome,(QTagID,QTagOutcome) x 5
class UserSelection(models.Model):
    outcome = models.BooleanField()
    suggested_dog = models.ForeignKey(Dog,on_delete=models.PROTECT)
    datetime = models.DateTimeField(auto_now=True)
    lat = models.FloatField()
    lng = models.FloatField()
    yes_list = models.CharField(max_length=128)
    no_list = models.CharField(max_length=128)

    def __str__(self):
        return str(self.datetime) + str(self.suggested_dog) + str(self.outcome)
