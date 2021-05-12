from django import forms
from .models import User
from django.contrib.auth import login, authenticate


class LoginValidate(forms.Form):
    username = forms.CharField(error_messages={'required': 'Username can not be empty'})
    password = forms.CharField(error_messages={'required': 'Password can not be empty'})

    def clean(self):
        username = str(self.cleaned_data.get('username'))
        password = str(self.cleaned_data.get('password'))
        if username is None or password is None:
            raise forms.ValidationError('Username or Password can not be empty')
        if User.objects.filter(username=username).count() != 0:
            user = User.objects.filter(username=username).first()
            if user.check_password(password):
                return True
            else:
                raise forms.ValidationError('Username or Password are not valid')
        else:
            raise forms.ValidationError('Username or Password are not valid1')
