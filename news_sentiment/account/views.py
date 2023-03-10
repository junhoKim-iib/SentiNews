from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import RegistrationForm, LoginForm
from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = 'account/home.html'



def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful')
            return redirect('account:login')
        
        else:
            # print specific error message for user to register and let them know what they did wrong
             for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field.capitalize()}: {error}')

    else: 
        form = RegistrationForm()

    return render(request, 'account/register.html', {'form': form})


def login_view(request): # login view
    if request.method == 'POST': # if the request is a POST request
        form = LoginForm(request.POST) # create a form instance and populate it with data from the request:
        if form.is_valid(): 
            email = form.cleaned_data['email'] 
            password = form.cleaned_data['password'] 
            user = authenticate(request, email=email, password=password) 
            if user is not None: 
                login(request, user) 
                return redirect('analysis:home') 
            else: 
                messages.error(request, 'Invalid email or password') 
    else:
        form = LoginForm()

    return render(request, 'account/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('account:login')


def mypage(request):
    return render(request, 'account/mypage.html', {})