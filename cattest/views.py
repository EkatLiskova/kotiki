from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView

from cattest.models import Test


class TestViews(APIView):
    def get(self, request):
        answers = Test.objects.all().get(id=1).answers
        return Response(data=answers, status=200)
