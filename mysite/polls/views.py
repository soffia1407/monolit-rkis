from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import Question, Choice, UserProfile
from django.template import loader
from django.urls import reverse
from django.views import generic
from .forms import UserRegistrationForm, UserProfileForm
from django.contrib import messages
from .forms import QuestionForm

@login_required
def create_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST, request.FILES) #Handle FILES now
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.save()
            messages.success(request, 'Вопрос успешно создан!')
            return redirect('polls:index')
        else:
            messages.error(request, 'Ошибка создания вопроса. Пожалуйста, проверьте данные.')
            # Optionally, provide more detailed error messages:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'Field "{field}": {error}')
            return render(request, 'polls/create_question.html', {'form': form})
    else:
        form = QuestionForm()
    return render(request, 'polls/create_question.html', {'form': form})


@login_required
def authenticated_index(request):
    questions = Question.objects.all()

    context = {
        'questions': questions,
        'user': request.user,
    }
    return render(request, 'polls/authenticated_index.html', {'user': request.user})


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            print("Message added successfully!")
            return redirect('polls:authenticated_index')
        else:
            messages.error(request, 'Registration failed. Please correct the errors below.')
            print("Form is invalid:", form.errors)
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'Field "{field}": {error}')
            return render(request, 'polls/register.html', {'form': form})
    else:
        form = UserRegistrationForm()
    return render(request, 'polls/register.html', {'form': form})

def index(request):
    if request.user.is_authenticated:
        return redirect('polls:authenticated_index')
    else:
        questions = Question.objects.all()
        context = {'questions': questions}
        return render(request, 'polls/index.html', context)

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('polls:authenticated_index')
    else:
        form = AuthenticationForm()
    return render(request, 'polls/login.html', {'form': form})


@login_required
def user_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user.userprofile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile Updated Successfully')
            return redirect('polls:profile')
    else:
        form = UserProfileForm(instance=request.user.userprofile)
    return render(request, 'polls/profile.html', {'form': form})


@login_required
def delete_profile(request):
    if request.method == 'POST':
        user = request.user
        user.delete()
        messages.success(request, 'Profile Deleted Successfully')
        return redirect('polls:login')
    return render(request, 'polls/delete_profile.html', {'user': request.user})

def logout_view(request):
    logout(request)
    messages.info(request, 'Logged Out Successfully')
    return redirect('polls:login')


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Question.objects.order_by('-pub_date')


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': 'вы не сделали выбор'
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
