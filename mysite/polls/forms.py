from django import forms
from django.contrib.auth.models import User
from .models import UserProfile
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
            UserProfile.objects.create(user=user)
        return user

class UserProfileForm(forms.ModelForm):
    avatar = forms.ImageField(required=True)

    class Meta:
        model = UserProfile
        fields = ('avatar',)