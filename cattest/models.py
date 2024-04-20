from django.db import models

# Create your models here.

class Test(models.Model):
    '''Информаиця о прохождении тестирования конкретного пользователя'''
    type_of_kotik = models.CharField(max_length=40, null=True)
    current_question = models.IntegerField(default=1)
    user_id = models.IntegerField(null=False)
    answers = models.CharField(blank=True, max_length=100) #(blank=True) может быть пуста строка

    class Meta:
        db_table = 'current_test'


class Question(models.Model):
    category = models.TextField(blank=True, null=True)
    text_of_question = models.TextField()
    number_of_question = models.IntegerField()

    class Meta:
        db_table = 'question'


class Result(models.Model):
    name_of_kotik = models.TextField(blank=True, null=True)
    number_of_kotik = models.IntegerField()
    number_of_picture = models.IntegerField()

    class Meta:
        db_table = 'result'




