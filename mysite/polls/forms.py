from django import forms  # Импортируем формы Django
from django.contrib.auth.models import User  # Импортируем модель User для работы с юзерами
from .models import UserProfile  # Импортируем модель UserProfile
from django.contrib.auth.forms import UserCreationForm  # Импортируем готовую форму создания юзера
from .models import Question  # Импортируем модель Question


class QuestionForm(forms.ModelForm):  # Форма для создания вопроса
    title =  forms.CharField(label='Question title')

    class Meta:  # Внутренний класс с настройками формы
        model = Question  # Привязываем форму к модели Question
        fields = ['title', 'text', 'image']  # Указываем поля, которые будут в форме
        widgets = {
            'text': forms.Textarea(attrs={'rows': 4, 'cols': 50}),
        }


class UserRegistrationForm(forms.ModelForm):  # Форма для регистрации юзера
    password = forms.CharField(widget=forms.PasswordInput)  # Пароль в форме (скрытый ввод)
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")
    avatar = forms.ImageField(required=False)  # Поле для аватара (не обязательно)

    class Meta:  # Настройки формы
        model = User  # Привязываем к модели User
        fields = ('username', 'first_name', 'last_name', 'email', 'password', 'password2', 'avatar')

    def clean_password2(self):  # Валидация: проверяем, что пароли совпадают
        cd = self.cleaned_data  # Получаем данные из формы
        if cd['password'] != cd['password2']:
            raise forms.ValidationError("Passwords don't match.")
        return cd['password2']

    def save(self, commit=True):  # Переопределяем сохранение формы
        user = super().save(commit=False)  # Создаём объект User, но не сохраняем сразу
        user.email = self.cleaned_data['email']  # Присваиваем email
        user.first_name = self.cleaned_data['first_name']  # Присваиваем имя
        user.last_name = self.cleaned_data['last_name']  # Присваиваем фамилию
        user.set_password(self.cleaned_data['password'])  # Задаём пароль
        if commit:  # Если нужно сохранить данные в БД
            user.save()  # Сохраняем пользователя
            UserProfile.objects.create(user=user, avatar=self.cleaned_data['avatar'])  # Создаём UserProfile
        return user  # Возвращаем пользователя



class UserEditForm(forms.ModelForm):  # Форма для редактирования юзера
    class Meta:  # Настройки формы
        model = User  # Привязываем к модели User
        fields = ('first_name', 'last_name', 'email')


class UserProfileForm(forms.ModelForm):  # Форма для редактирования профиля юзера
    class Meta:  # Настройки формы
        model = UserProfile  # Привязываем к модели UserProfile
        fields = ('avatar', 'bio', 'phone_number')