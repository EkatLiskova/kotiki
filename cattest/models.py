from django.db import models

# Create your models here.

class Test(models.Model):
    type_of_kotik = models.IntegerField(null=True) #(null=True) пусто если тест не окончен
    current_question = models.IntegerField(default=1)
    user_id = models.IntegerField(null=False)
    answers = models.CharField(blank=True, max_length=100) #(blank=True) может быть пуста строка

    class Meta:
        db_table = 'current_test'


class Question(models.Model):
    text_of_question = models.TextField()
    number_of_question = models.IntegerField()

    class Meta:
        db_table = 'question'





