"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.contrib import admin # Импортируем админку Django. Это как панель управления сайтом для админов
from django.urls import path, include # Импортируем функции для работы с URL-ами

urlpatterns = [ # Создаём список всех URL-ов нашего сайта
    path('', include('polls.urls')), # Если пользователь заходит на главную страницу (''),то перенаправляем его в файл urls.py приложения polls
    path('admin/', admin.site.urls), # Это URL для админки. Когда заходим на /admin, попадаем в панель управления Django
    path('accounts/', include('django.contrib.auth.urls')), # Это URL для аутентификации.