import datetime  # Импортируем модуль для работы с датой и временем

from django.db import models  # Импортируем модели Django
from django.utils import timezone  # Импортируем утилиты для работы с часовыми поясами
from django.contrib.auth.models import User  # Импортируем модель User
from django.urls import reverse  # Импортируем функцию для генерации URL-ов

class UserProfile(models.Model):  # Модель для профиля пользователя
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userprofile')
    # Один-к-одному отношение к модели User (один юзер - один профиль)
    avatar = models.ImageField(upload_to='profile_avatars/', blank=True, null=True)
    # Аватар пользователя (картинка), может быть пустым
    bio = models.TextField(blank=True, null=True)  # Биография пользователя, может быть пустой
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    # Номер телефона пользователя, может быть пустым

    def __str__(self):
        return self.user.username  # Возвращает имя пользователя при запросе модели

    def get_absolute_url(self):
        return reverse('polls:profile', args=[str(self.user.id)]) # Возвращает URL на страницу профиля, используя id пользователя


class Question(models.Model):  # Модель для вопроса
    title = models.CharField(max_length=200)
    text = models.TextField()
    image = models.ImageField(upload_to='question_images/', blank=True, null=True)  # Картинка вопроса, может быть пустой
    author = models.ForeignKey(User, on_delete=models.CASCADE) # Автор вопроса (связь с моделью User), если юзер удаляется то вопрос тоже
    pub_date = models.DateTimeField('date published', default=timezone.now)

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1) # Проверяет, был ли вопрос опубликован недавно (за последние 24 часа)

    def __str__(self):
        return self.title  # Возвращает заголовок вопроса при запросе модели


class Choice(models.Model):  # Модель для варианта ответа на вопрос
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    # Вопрос, к которому относится вариант ответа (если вопрос удаляется то ответы тоже)
    choice_text = models.CharField(max_length=200)  # Текст варианта ответа
    votes = models.IntegerField(default=0)  # Количество голосов за этот вариант

    def __str__(self):
        return self.choice_text  # Возвращает текст варианта ответа при запросе модели