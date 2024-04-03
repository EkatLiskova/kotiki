from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from cattest.models import Test, Question


class TestViews(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        username = request.user  # при обычном входе
        id = User.objects.all().get(username=username).id
        answers = Test.objects.all().get(id=id).answers
        return HttpResponse(answers)


class RegisterViews(APIView):
    def post(self, request):
        name = request.data.get('name') #при регистрации
        mail = request.data.get('mail')
        password = request.data.get('password')
        User.objects.create_user(name, mail, password)
        return Response(status=201)


class QuestionViews(APIView):

    def get_question(self):
        user_id = 1
        number_of_question = Test.objects.all().get(user_id=user_id).current_question
        text_of_question = Question.objects.all().get(number_of_question=number_of_question).text_of_question
        return {'textik': text_of_question}

    def get(self, request):
        user_id = 1
        user_test_info = Test.objects.all().get(user_id=user_id)
        if user_test_info.current_question > 28:
            return render(request, 'Результат теста.html')
        return render(request, 'Прохождение теста.html', context=self.get_question())

    def post(self, request):
        user_id = 1
        user_test_info = Test.objects.all().get(user_id=user_id)
        button_answer = request.data.get('button_answer')
        user_test_info.answers = user_test_info.answers + button_answer
        user_test_info.current_question = user_test_info.current_question + 1
        user_test_info.save()
        if user_test_info.current_question <= 28:
            return render(request, 'Прохождение теста.html', context=self.get_question())
        else:
            #тут будет вычисляться результат
            return render(request, 'Результат теста.html')


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
        return render(request, 'Кнопка начала теста.html')






