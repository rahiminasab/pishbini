from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(max_length=100, required=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'password1', 'password2',)

    def clean(self):
        cleaned_data = super(SignUpForm, self).clean()
        email = cleaned_data.get('email')
        username = cleaned_data.get('username')
        if User.objects.filter(email=email).exclude(username=username).exists():
            raise forms.ValidationError(u'Email addresses must be unique.')
        return cleaned_data


class UserActivationRequiredForm(forms.Form):
    email_input = forms.EmailField(max_length=100, required=True)

    class Meta:
        fields = ('email_input',)


class ResetPassInitForm(forms.Form):
    email_input = forms.EmailField(max_length=100, required=True)

    class Meta:
        fields = ('email_input',)

    def clean(self):
        cleaned_data = super(ResetPassInitForm, self).clean()
        email = cleaned_data.get('email_input')
        try:
            User.objects.get(email=email)
            return cleaned_data
        except User.DoesNotExist:
           raise forms.ValidationError(u'User with this Email address is not found!')


class ResetPassConfirmForm(forms.Form):
    password = forms.CharField(max_length=30, required=True)
    password_repeat = forms.CharField(max_length=30, required=True)

    class Meta:
        fields = ('password', 'password_repeat')

    def clean(self):
        cleaned_data = super(ResetPassConfirmForm, self).clean()
        pass1 = cleaned_data.get('password')
        pass2 = cleaned_data.get('password_repeat')
        if pass1 != pass2:
            raise forms.ValidationError(u'The two provided passwords are not the same!')