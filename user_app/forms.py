from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError


User = get_user_model()


def email_validator(value):
    taken_emails = User.objects.filter(email=value)
    if taken_emails:
        raise ValidationError('Email jest zajęty')


class RegisterForm(forms.ModelForm):
    password2 = forms.CharField(required=True,
                                widget=forms.PasswordInput(attrs={'placeholder': 'Powtórz hasło', 'class': "form-control"}))
    email = forms.EmailField(max_length=150, required=True, validators=[email_validator],
                             widget=forms.EmailInput(attrs={'placeholder': 'Email', 'class': "form-control"}))

    class Meta:
        model = User
        fields = ['first_name', 'email', 'imdb_link', 'password', 'password2']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Imię', 'class': "form-control"}),
            'imdb_link': forms.URLInput(attrs={'placeholder': 'Lista IMDb', 'class': "form-control"}),
            'password': forms.PasswordInput(attrs={'placeholder': 'Hasło', 'class': "form-control"}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')
        if password != password2:
            raise forms.ValidationError('Hasła nie są identyczne')


class LoginForm(forms.Form):
    email = forms.EmailField(max_length=150, required=True, widget=forms.EmailInput(
        attrs={'placeholder': 'Email', 'class': "form-control"}))
    password = forms.CharField(max_length=120, required=True, widget=forms.PasswordInput(
        attrs={'placeholder': 'Hasło', 'class': "form-control"}))
