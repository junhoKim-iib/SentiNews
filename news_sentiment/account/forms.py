from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from .models import User


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')
        if email and password:
            self.user = authenticate(email=email, password=password)
            if self.user is None:
                raise forms.ValidationError('Invalid email or password')
        return cleaned_data
    
    def get_user(self):
        return self.user
    

# 비밀번호 변경 폼. 기존 비밀번호, 새 비밀번호, 새 비밀번호 확인을 입력받는다.
# 기존 비밀번호가 일치하지 않으면 에러 메시지를 출력한다.
# 새 비밀번호와 새 비밀번호 확인이 일치하지 않으면 에러 메시지를 출력한다.
# 비밀번호 변경에 성공하면 로그인 페이지로 이동한다.

class PasswordChangeForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput)
    new_password = forms.CharField(widget=forms.PasswordInput)
    new_password_confirm = forms.CharField(widget=forms.PasswordInput)


    def clean(self):
        cleaned_data = super(PasswordChangeForm, self).clean()
        old_password = cleaned_data.get('old_password')
        new_password1 = cleaned_data.get('new_password1')
        new_password2 = cleaned_data.get('new_password2')
        print(old_password, new_password1, new_password2)
        if old_password and new_password1 and new_password2:
            if not self.user.check_password(old_password):
                raise forms.ValidationError('Invalid old password')
            if new_password1 != new_password2:
                raise forms.ValidationError('New password does not match')
        return cleaned_data

    def save(self):
        self.user.set_password(self.cleaned_data['new_password'])
        self.user.save()

    def set_user(self, user):
        self.user = user    


