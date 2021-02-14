from django import forms
from django.contrib.auth.hashers import check_password
from .models import User

class RegisterForm(forms.Form):
    username = forms.CharField(error_messages={'required':'아이디를 입력해주세요.'}, max_length=128, label='Username')
    email = forms.EmailField(error_messages={'required':'이메일을 입력해주세요'}, max_length=128, label='E-mail')
    password = forms.CharField(error_messages={'required':'비밀번호를 입력해주세요'}, widget=forms.PasswordInput, label='비밀번호')
    re_password = forms.CharField(error_messages={'required':'비밀번호를 입력해주세요'}, widget=forms.PasswordInput, label='비밀번호 확인')

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')
        re_password = cleaned_data.get('re_password')

        if password and re_password:
            if password != re_password:
                self.add_error('re_password','입력하신 비밀번호들이 일치가 안됩니다.')


        if username:
            try:
                user = User.objects.get(username=username)
                if user:
                    self.add_error('username', '아이디를 이미 존재합니다.')
            except User.DoesNotExist:
                pass

class LoginForm(forms.Form):
    username = forms.CharField(error_messages={'required':'Username 을 입력해주세요'},max_length=128, label='ID')
    password = forms.CharField(error_messages={'required':'비밀번호를 입력해주세요.'}, widget=forms.PasswordInput, label='비밀번호')

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password  = cleaned_data.get('password')

        if username and password:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                self.add_error('username', '아이디나 비밀번호가 맞지 않습니다.')

            if not check_password(password, user.password):
                self.add_error('username', '아이디나 비빌번호가 맞지 않습니다')