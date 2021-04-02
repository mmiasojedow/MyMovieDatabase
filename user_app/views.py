from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views import View

from user_app.forms import RegisterForm, LoginForm

User = get_user_model()


class RegisterView(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, 'user_app/register.html', {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            email = form.cleaned_data['email']
            imdb_link = form.cleaned_data['imdb_link']
            password = form.cleaned_data['password']
            User.objects.create_user(
                username=email, first_name=first_name, email=email, password=password, imdb_link=imdb_link)
            return redirect('login')
        else:
            return render(request, 'user_app/register.html', {'form': form})


class LoginView(View):
    def get(self, request):
        form = LoginForm()
        header = 'Logowanie'
        return render(request, 'user_app/login.html', {'form': form, 'header': header})

    def post(self, request):
        form = LoginForm(request.POST)
        header = 'Wypełnij poprawnie formularz'
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(username=email, password=password)
            if user is not None:
                login(request, user)
                url = request.GET.get('next') if request.GET.get(
                    'next') is not None else 'main'
                return redirect(url)
            else:
                return render(request, 'user_app/login.html',
                              {'form': form, 'header': 'Błędny email lub hasło'})
        else:
            return render(request, 'user_app/login.html', {'form': form, 'header': header})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('main')
