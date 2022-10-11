from typing import Any
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm

from core.models import Gift, GiftCardRequest, News, Replacement, Retirement, User, Vacation


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
            'first_name',
            'last_name',
            'email',
            'zip_code',
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
            'email',
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
            'solider_first_name',
            'solider_last_name',
            'solider_id_number',
            'internet_card_image',
            'internet_card_number',
            'internet_card_amount',
            'internet_card_type',
        ]


class UserLoginForm(forms.Form):
    military_id = forms.TextInput()
    password = forms.PasswordInput()


class CheckStatusForm(forms.Form):
    CATEGORIES =(
        ("vacation", "Vacation"),
        ("retirement", "Retirement"),
        ("replacement", "Replacement"),
        ("card_purchase", "Internet Card"),
    )
    code = forms.CharField(max_length=50, required=True)
    category = forms.ChoiceField(choices=CATEGORIES)


class VacationForm(forms.ModelForm):
    class Meta:
        model = Vacation
        fields = '__all__'


class GiftCardRequestForm(forms.ModelForm):
    class Meta:
        model = GiftCardRequest
        fields = '__all__'


class NewsCreationForm(forms.ModelForm):
    class Meta:
        model = News
        fields = '__all__'

