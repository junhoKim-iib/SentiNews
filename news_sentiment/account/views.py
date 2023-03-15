from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import RegistrationForm, LoginForm



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


@login_required
def logout_view(request):
    logout(request)
    return redirect('account:login')



@login_required
def mypage(request):
    user = request.user
    # 비밀번호 변경 폼 처리
    if request.method == 'POST':
        form = PasswordChangeForm(user=user, data=request.POST)
        print(form)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, '비밀번호가 변경되었습니다.')
            return redirect('account:mypage')
       
            
    else:
        
        form = PasswordChangeForm(user=user)
    
    return render(request, 'account/mypage.html', {'form': form})
    

@login_required
def delete_account(request):
    if request.method == 'POST':
        user = request.user
        user.delete()
        messages.success(request, '회원 탈퇴가 완료되었습니다.')
        return redirect('analysis:home')
    return render(request, 'account/delete_account.html')