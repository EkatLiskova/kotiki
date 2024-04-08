from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from cattest.models import Test, Question
from saitik3.settings import COUNT_OF_QUESTION


class RegisterViews(APIView):
    def post(self, request):
        name = request.data.get('name') #при регистрации
        mail = ''
        password = request.data.get('password')
        User.objects.create_user(name, mail, password)
        return redirect('Начало')

    def get(self, request):
        return render(request, 'регистрация.html')


class QuestionViews(APIView):

    def get_question(self):
        user_id = 1
        number_of_question = Test.objects.all().get(user_id=user_id).current_question
        text_of_question = Question.objects.all().get(number_of_question=number_of_question).text_of_question
        return {'textik': text_of_question}

    def get(self, request):
        user_id = 1
        user_test_info = Test.objects.all().get(user_id=user_id)
        if user_test_info.current_question > COUNT_OF_QUESTION:
            return redirect('Результат')
        return render(request, 'Прохождение теста.html', context=self.get_question())

    def post(self, request):
        user_id = 1
        user_test_info = Test.objects.all().get(user_id=user_id)
        button_answer = request.data.get('button_answer')
        user_test_info.answers = user_test_info.answers + button_answer
        user_test_info.current_question = user_test_info.current_question + 1
        user_test_info.save()
        if user_test_info.current_question <= COUNT_OF_QUESTION:
            return render(request, 'Прохождение теста.html', context=self.get_question())
        else:
            #тут будет вычисляться результат
            return redirect('Результат')


def result(answers):
    baza = ''
    active = ''
    communication = ''
    for e, i in enumerate(answers):
        category = Question.objects.all().get(number_of_question=e + 1).category
        if category == 'baza':
            baza = baza + i
        elif category == 'active':
            active = active + i
        elif category == 'communication':
            communication = communication + i

    is_active = True if active.count('1') > 3 else False
    is_communication = True if communication.count('1') > 3 else False

class StartViews(APIView):
    def get(self, request): #request это любые данные, которые передаются в запросе на сервер
        is_auntificated = False
        if not is_auntificated:
            return redirect('Логин')
        user_id = 1
        user_test_info = Test.objects.all().get(user_id=user_id)
        if user_test_info.current_question > COUNT_OF_QUESTION:
            return redirect('Результат')
        elif user_test_info.current_question > 1:
            return redirect('Вопрос')
        else:
            return render(request, 'Кнопка начала теста.html')


class ResultView(APIView):
    def get(self, request):
        return render(request, 'Результат теста.html')

    def post(self, request):
        user_id = 1
        user_test_info = Test.objects.all().get(user_id=user_id)
        user_test_info.answers = ''
        user_test_info.current_question = 1
        user_test_info.type_of_kotik = None
        user_test_info.save()
        return redirect('Начало')


class LoginView(APIView):
    def post(self, request):
        return redirect('Регистрация')

    def get(self, request):
        return render(request, 'вход.html')











