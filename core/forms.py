from typing import Any
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm

from core.models import Retirement, User


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = '__all__'
        exclude = ['date_joined', 'password']

    # def save(self, commit=False) -> Any:
    #     user = super().save()
    #     user.set_password(self.instance.password)
    #     super().save(commit=True)
    #     return user



class RetirementForm(forms.ModelForm):
    class Meta:
        model = Retirement
        fields = [
            'address',
            'city',
            'region',
            'phone_number',
            'ceremony_date',
            'rank',
            'branch_of_service',
            'years_of_service',
            'date_of_retirement',
            'additional_information',
        ]


class UserLoginForm(forms.Form):
    military_id = forms.TextInput()
    password = forms.PasswordInput()


