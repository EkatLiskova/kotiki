"""
URL configuration for saitik3 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from cattest.views import RegisterViews, QuestionViews, StartViews, ResultView, LoginView, CheckView, LogOutView
from saitik3 import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('reg/', RegisterViews.as_view(), name='Регистрация'),
    path('question/', QuestionViews.as_view(), name='Вопрос'),
    path('', CheckView.as_view(), name='Проверка'),
    path('start/', StartViews.as_view(), name='Начало'),
    path('result/', ResultView.as_view(), name='Результат'),
    path('login/', LoginView.as_view(), name='Логин'),
    path('logout/', LogOutView.as_view(), name='Логаут'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
