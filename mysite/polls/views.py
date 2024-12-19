from django.contrib.auth import authenticate, login, logout  # Функции для аутентификации
from django.contrib.auth.decorators import login_required  # Декоратор для защиты страниц
from django.contrib.auth.forms import AuthenticationForm  # Готовая форма для входа
from django.shortcuts import render, get_object_or_404, redirect  # Функции для рендеринга страниц
from django.http import HttpResponse, HttpResponseRedirect  # HTTP-ответы
from .models import Question, Choice, UserProfile  # Наши модели
from django.urls import reverse  # Для получения URL по имени
from django.views import generic  # Для view на основе классов
from .forms import UserRegistrationForm, UserProfileForm  # Наши формы
from django.contrib import messages  # Для вывода сообщений пользователю
from .forms import QuestionForm  # Наша форма для вопросов

@login_required  # Только для авторизованных пользователей
def create_question(request):  # Функция создания вопроса
    if request.method == 'POST':  # Если форма отправлена
        form = QuestionForm(request.POST, request.FILES)  # Заполняем форму данными
        if form.is_valid():  # Если данные в форме валидны
            question = form.save(commit=False)  # Создаём объект вопроса, но не сохраняем
            question.author = request.user  # Записываем автора вопроса (текущего пользователя)
            question.save()  # Сохраняем вопрос
            messages.success(request, 'Вопрос успешно создан!')  # Сообщение об успехе
            return redirect('polls:index')  # Перенаправляем на главную страницу
        else:  # Если данные в форме не валидны
            messages.error(request, 'Ошибка создания вопроса. Пожалуйста, проверьте данные.')
             # Сообщение об ошибке
            for field, errors in form.errors.items():
                for error in errors:
                     messages.error(request, f'Field "{field}": {error}')
            return render(request, 'polls/create_question.html', {'form': form})  # Возвращаем форму с ошибками
    else:  # Если форма не отправлена
        form = QuestionForm()  # Создаём пустую форму
    return render(request, 'polls/create_question.html', {'form': form})


@login_required  # Только для авторизованных пользователей
def authenticated_index(request):  # Функция для главной страницы для авторизованных
    questions = Question.objects.all()  # Получаем все вопросы
    context = {
        'questions': questions,  # Передаём вопросы в шаблон
        'user': request.user,
    }
    return render(request, 'polls/authenticated_index.html', context)


def register(request):  # Функция регистрации
    if request.method == 'POST':  # Если форма отправлена
        form = UserRegistrationForm(request.POST, request.FILES)  # Заполняем форму данными
        if form.is_valid():  # Если данные в форме валидны
            user = form.save()  # Сохраняем юзера
            login(request, user)  # Логиним юзера
            messages.success(request, 'Registration successful!')  # Сообщение об успехе
            print("Message added successfully!")
            return redirect('polls:authenticated_index')  # Перенаправляем на главную страницу
        else:  # Если данные в форме не валидны
            messages.error(request, 'Registration failed. Please correct the errors below.')
            print("Form is invalid:", form.errors)
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'Field "{field}": {error}')
            return render(request, 'polls/register.html', {'form': form})
    else:  # Если форма не отправлена
        form = UserRegistrationForm()  # Создаём пустую форму
    return render(request, 'polls/register.html', {'form': form})

def index(request):  # Функция для главной страницы
    if request.user.is_authenticated:  # Проверяем, авторизован ли юзер
        return redirect('polls:authenticated_index')  # Если да, перенаправляем на страницу для авторизованных
    else:  # Если нет
        questions = Question.objects.all()  # Получаем все вопросы
        context = {'questions': questions}  # Передаём вопросы в шаблон
        return render(request, 'polls/index.html', context)

def login_view(request):  # Функция для входа
    if request.method == 'POST':  # Если форма отправлена
        form = AuthenticationForm(request, data=request.POST)  # Заполняем форму данными
        if form.is_valid():  # Если данные в форме валидны
            user = form.get_user()  # Получаем юзера
            login(request, user)  # Логиним юзера
            return redirect('polls:authenticated_index')  # Перенаправляем на главную страницу
    else:  # Если форма не отправлена
        form = AuthenticationForm()  # Создаём пустую форму
    return render(request, 'polls/login.html', {'form': form})


@login_required
def user_profile(request, user_id): # Функция для просмотра и редактирования профиля пользователя
    user = get_object_or_404(User, id=user_id) # Получаем пользователя по id, или 404 ошибка
    if request.method == 'POST': # Если форма отправлена
        form = UserProfileForm(request.POST, request.FILES, instance=user.userprofile) # Заполняем форму данными профиля
        if form.is_valid(): # Если данные в форме валидны
            form.save() # Сохраняем профиль
            messages.success(request, 'Profile Updated Successfully') # Сообщение об успехе
            return redirect('polls:profile', user_id=user_id) # Перенаправляем на страницу профиля
    else: # Если форма не отправлена
        form = UserProfileForm(instance=user.userprofile) # Создаём форму с данными профиля

    return render(request, 'polls/profile.html', {'form': form, 'user': user})

@login_required
def delete_profile(request): # Функция для удаления профиля пользователя
    if request.method == 'POST': # Если форма отправлена
        user = request.user # Получаем текущего пользователя
        user.delete() # Удаляем пользователя
        messages.success(request, 'Profile Deleted Successfully') # Сообщение об успехе
        return redirect('polls:login') # Перенаправляем на страницу входа
    return render(request, 'polls/delete_profile.html', {'user': request.user})

def logout_view(request):
    logout(request)  # Выходим из аккаунта
    messages.info(request, 'Logged Out Successfully')  # Сообщение об успехе
    return redirect('polls:index')  # Перенаправляем на главную страницу


class IndexView(generic.ListView): # Класс для главной страницы (список вопросов)
    template_name = 'polls/index.html' # Путь к шаблону
    context_object_name = 'latest_question_list' # Переменная, с которой данные приходят в шаблон

    def get_queryset(self): # Получаем данные (список вопросов)
        return Question.objects.order_by('-pub_date') # Сортируем вопросы по дате (новые сначала)


class DetailView(generic.DetailView): # Класс для страницы с деталями вопроса
    model = Question # Указываем модель
    template_name = 'polls/detail.html' # Путь к шаблону


class ResultsView(generic.DetailView): # Класс для страницы с результатами голосования
    model = Question # Указываем модель
    template_name = 'polls/results.html' # Путь к шаблону


def vote(request, question_id): # Функция для обработки голосования
    question = get_object_or_404(Question, pk=question_id) # Получаем вопрос по id
    try: # Пытаемся получить вариант ответа
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist): # Если вариант ответа не найден, то выводим ошибку
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': 'вы не сделали выбор'
        })
    else:
        selected_choice.votes += 1  # Увеличиваем количество голосов
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))  # Перенаправляем на страницу с результатами
