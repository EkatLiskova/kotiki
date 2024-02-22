from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from cattest.models import Test


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