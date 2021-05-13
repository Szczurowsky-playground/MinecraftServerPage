from django import forms
from .models import User
from django.core.validators import validate_email, validate_slug
from django.contrib.auth.password_validation import validate_password


class SecurityValidate(forms.Form):
    email_new = forms.CharField(required=False)
    password_new = forms.CharField(required=False)
    password = forms.CharField(error_messages={'required': 'Password can not be empty'})

    def clean(self):
        email_new = str(self.cleaned_data.get('email_new'))
        password_new = str(self.cleaned_data.get('password_new'))
        password = str(self.cleaned_data.get('password'))
        if password is None:
            raise forms.ValidationError('Password can not be empty')
        if password_new is None and email_new is None:
            raise forms.ValidationError('You do not changing anything')
        if email_new is not None and email_new is not '':
            try:
                validate_email(email_new)
            except forms.ValidationError:
                raise forms.ValidationError("Email is not correct")
        if password_new is not None and password_new is not '':
            try:
                validate_password(password_new, self)
            except forms.ValidationError as error:
                raise forms.ValidationError(error)
        return True


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


class RegisterValidate(forms.Form):
    username = forms.CharField(error_messages={'required': 'Username can not be empty'})
    nickname = forms.CharField(error_messages={'required': 'Nickname can not be empty'})
    email = forms.CharField(error_messages={'required': 'Email address can not be empty'})
    password = forms.CharField(error_messages={'required': 'Password can not be empty'})
    password2 = forms.CharField(error_messages={'required': 'Please retype the password'})
    tos = forms.BooleanField(required=False)

    def clean(self):
        username = str(self.cleaned_data.get('username'))
        nickname = str(self.cleaned_data.get('nickname'))
        email = str(self.cleaned_data.get('email'))
        password = str(self.cleaned_data.get('password'))
        password2 = str(self.cleaned_data.get('password2'))
        tos = self.cleaned_data.get('tos')
        try:
            validate_email(email)
        except forms.ValidationError:
            raise forms.ValidationError("Email is not correct")
        try:
            validate_slug(username)
        except forms.ValidationError:
            raise forms.ValidationError("Username is not correct")
        try:
            validate_slug(nickname)
        except forms.ValidationError:
            raise forms.ValidationError("Nickname is not correct")
        try:
            validate_password(password, self)
        except forms.ValidationError as error:
            raise forms.ValidationError(error)
        if password != password2:
            raise forms.ValidationError('Passwords are not identical')
        if tos is False:
            raise forms.ValidationError('ToS need to be accepted')
        if User.objects.filter(username=username).count() != 0:
            raise forms.ValidationError('Username already exists')
        if User.objects.filter(nickname=nickname).count() != 0:
            raise forms.ValidationError('Nickname already exists')
        if User.objects.filter(email=email).count() != 0:
            raise forms.ValidationError('Email is already claimed')
        return True
