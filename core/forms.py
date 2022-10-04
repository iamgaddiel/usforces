from typing import Any
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm

from core.models import Gift, Replacement, Retirement, User


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



class ReplacementForm(forms.ModelForm):
    class Meta:
        model = Replacement
        fields = [
            'name_of_soldier',
            'rank_of_soldier',
            'base_of_current_service',
            'destination_after_replacement',
            'name_of_applicant',
            'country_of_origin_or_location',
            'relationship_to_the_soldier',
            'applicants_id_number',
            'applicants_address',
        ]


class GiftCreationForm(forms.ModelForm):
    class Meta:
        model = Gift
        fields = [
            'solders_id_number',
            'solder_first_name',
            'solder_last_name',
            'gift_image',
            'git_card_number',
            'gift_card_amount',
            'gift_card_type',
        ]


class UserLoginForm(forms.Form):
    military_id = forms.TextInput()
    password = forms.PasswordInput()


