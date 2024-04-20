from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from cattest.models import Test, Question, Result
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

def is_anonim(request):
    if 'Anonim' in str(request.user):
        return 'anonim'
    else:
        return 'not anonim'

class QuestionViews(APIView):

    def get_question(self, request):
        id = User.objects.all().get(username=request.user).id
        number_of_question = Test.objects.all().get(user_id=id).current_question
        text_of_question = Question.objects.all().get(number_of_question=number_of_question).text_of_question
        return text_of_question

    def get(self, request):
        id = User.objects.all().get(username=request.user).id
        user_test_info = Test.objects.all().get(user_id=id)
        if user_test_info.current_question > COUNT_OF_QUESTION:
            return redirect('Результат')
        return render(request, 'Прохождение теста.html', context={'textik':self.get_question(request), 'Anonim': is_anonim(request)})

    def post(self, request):
        id = User.objects.all().get(username=request.user).id
        user_test_info = Test.objects.all().get(user_id=id)
        button_answer = request.data.get('button_answer')
        user_test_info.answers = user_test_info.answers + button_answer
        user_test_info.current_question = user_test_info.current_question + 1
        user_test_info.save()
        if user_test_info.current_question <= COUNT_OF_QUESTION:
            return render(request, 'Прохождение теста.html',  context={'textik':self.get_question(request), 'Anonim': is_anonim(request)})
        else:
            user_test_info.type_of_kotik = result(user_test_info.answers)[0]
            user_test_info.save()
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

    is_active = '1' if active.count('1') > 3 else '2'
    is_communication = '1' if communication.count('1') > 3 else '2'
    answer = baza + is_active + is_communication
    result_of_name = {'1111': 'Домашний пумба',
                      '1112': 'Сладкий пирожок',
                      '1121': 'Мягонький кексик',
                      '1122': 'Водяной подкрадун',
                      '1211': 'Социальный круглун',
                      '1212': 'Комнатный летун',
                      '1221': 'Лучезарный Плюш',
                      '1222': 'Тихий Гурман',
                      '2111': '????????',
                      '2112': 'Красивый Шпион',
                      '2121': 'Лев Зверей',
                      '2122': 'Надушенный Пиончик',
                      '2211': 'Дружелюбный Мурчун',
                      '2212': 'Неугомонный Кексик',
                      '2221': 'Диванный Мурлотень',
                      '2222': 'Уютный затворник'}
    name_of_kotik = Result.objects.all().get(number_of_kotik=answer).name_of_kotik
    number_of_picture = Result.objects.all().get(number_of_kotik=answer).number_of_picture
    return name_of_kotik, number_of_picture



class StartViews(APIView):
    def get(self, request): #request это любые данные, которые передаются в запросе на сервер
        id = User.objects.all().get(username=request.user).id
        user_test_info = Test.objects.all().get(user_id=id)
        if user_test_info.current_question > COUNT_OF_QUESTION:
            return redirect('Результат')
        elif user_test_info.current_question > 1:
            return redirect('Вопрос')
        else:
            return render(request, 'Кнопка начала теста.html', context={'Anonim': is_anonim(request)})



class ResultView(APIView):

    def get(self, request):
        id = User.objects.all().get(username=request.user).id
        user_test_info = Test.objects.all().get(user_id=id)
        return render(request, 'Результат теста.html', context={'name_of_kotik': user_test_info.type_of_kotik, 'Picture': Result.objects.all().get(name_of_kotik=user_test_info.type_of_kotik).number_of_picture, 'Anonim':is_anonim(request)})

    def post(self, request):
        id = User.objects.all().get(username=request.user).id
        user_test_info = Test.objects.all().get(user_id=id)
        user_test_info.answers = ''
        user_test_info.current_question = 1
        user_test_info.type_of_kotik = None
        user_test_info.save()
        print(request.user)

        if 'Anonim' in str(request.user):
            return redirect('Логин')
        else:
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
        if not request.user.is_authenticated:
            return redirect('Логин')
        else:
            return redirect('Начало')


class LogOutView(APIView):

    def post(self, request):
        logout(request)
        return redirect('Логин')








