from django.contrib.auth import authenticate, login
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
        button_answer = request.data.get('button_answer')
        if button_answer == 1:
            name = request.data.get('name') #при регистрации
            chek = User.objects.all().filter(username=name)
            password = request.data.get('password')
            if chek:#TODO: сделать в html уведомление о том, что такой логин уже существует
                return render(request, 'регистрация.html')
        else:#cоздание анонимного пользователя #TODO: сделать, чтобы анонимус удалялся
            colvo_of_user = len(User.objects.all())
            name = 'Anonim' + str(colvo_of_user)
            chek1 = User.objects.all().filter(username=name)
            if chek1:
                name = name + 'povtor'
            password = name
        User.objects.create_user(name, '', password)# '' это типа маил
        id = User.objects.all().get(username=name).id
        Test.objects.create(type_of_kotik=None, current_question=1, user_id=id, answers='')
        user = authenticate(request, username=name, password=password)
        login(request, user)
        return redirect('Начало')

    def get(self, request):
        return render(request, 'регистрация.html')


class QuestionViews(APIView):

    def get_question(self, request):
        id = User.objects.all().get(username=request.user).id
        number_of_question = Test.objects.all().get(user_id=id).current_question
        text_of_question = Question.objects.all().get(number_of_question=number_of_question).text_of_question
        return {'textik': text_of_question}

    def get(self, request):
        id = User.objects.all().get(username=request.user).id
        user_test_info = Test.objects.all().get(user_id=id)
        if user_test_info.current_question > COUNT_OF_QUESTION:
            return redirect('Результат')
        return render(request, 'Прохождение теста.html', context=self.get_question(request))

    def post(self, request):
        id = User.objects.all().get(username=request.user).id
        user_test_info = Test.objects.all().get(user_id=id)
        button_answer = request.data.get('button_answer')
        user_test_info.answers = user_test_info.answers + button_answer
        user_test_info.current_question = user_test_info.current_question + 1
        user_test_info.save()
        print(request.user)
        if user_test_info.current_question <= COUNT_OF_QUESTION:
            return render(request, 'Прохождение теста.html', context=self.get_question(request))
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
        id = User.objects.all().get(username=request.user).id
        user_test_info = Test.objects.all().get(user_id=id)
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
        id = User.objects.all().get(username=request.user).id
        user_test_info = Test.objects.all().get(user_id=id)
        user_test_info.answers = ''
        user_test_info.current_question = 1
        user_test_info.type_of_kotik = None
        user_test_info.save()
        return redirect('Начало')


class LoginView(APIView):
    def post(self, request):
        name = request.data.get('name')
        password = request.data.get('password')
        user = authenticate(request, username=name, password=password)
        if user is None:
            return render(request, 'вход.html')
        else:
            login(request, user)
            return redirect('Начало')

    def get(self, request):
        return render(request, 'вход.html')


class CheckView(APIView):
    def get(self, request):
        is_auntificated = False
        if not is_auntificated:
            return redirect('Логин')
        else:
            return redirect('Начало')








