from ast import Dict
from http.client import HTTPResponse
import json
from typing import Any
from django.forms import BaseModelForm

from django.http import HttpResponse
from django.forms.models import model_to_dict
from django.shortcuts import render
from django.views.generic import (
    TemplateView,
    DetailView,
    DeleteView,
    CreateView,
    ListView,
    View
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import  LoginView
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy
from django.shortcuts import redirect, resolve_url
from django.core import serializers

from core.forms import CustomUserCreationForm, GiftCreationForm, ReplacementForm, RetirementForm, UserCreationForm, UserLoginForm
from core.models import Gift, Replacement, Retirement, User
from core.utils import get_random_string



def index(request):
    template_name = 'core/index.html'
    return render(request, template_name)


class AdminLoginView(LoginView):
    template_name = 'core/admin_login.html'

    def post(self, request, *args, **kwargs) -> HTTPResponse:
        try:
            email  = request.POST.get('username', None)
            password = request.POST.get('password', None)

            user =  User.objects.get(email=email)
            if (user := authenticate(request, email=email, password=password)) is None:
                context = {
                    'error': 'Access denied'
                }
                return render(request, self.template_name)
            login(request, user)

            
        except User.DoesNotExist as e:
            context = {
                    'error': 'No user with this details'
                }
            return render(request, self.template_name, context)
        return super().post(request, *args, **kwargs)





# ---------------------------------------------------------
# ----------------- [ Admin User Section ] ----------------  
# ---------------------------------------------------------
def admin_logout(request):
    logout(request)
    return redirect('core:admin_login')


class AdminDashboard(LoginRequiredMixin, TemplateView):
    template_name = 'core/admin_dashboard.html'
    extra_context = {
        'users': User.objects.all(),
        'replacements': Replacement.objects.all(),
        'gifts': Gift.objects.all(),
        'retires': Retirement.objects.all()
    }


class AdminUserList(LoginRequiredMixin, ListView):
    context_object_name = 'users'
    template_name = 'core/admin_list_user.html'

    def get_queryset(self):
        return User.objects.exclude(email='admin@gmail.com')


class AdminUserCreate(LoginRequiredMixin, CreateView):
    template_name = 'core/admin_dashboard_add_user.html'
    model = User
    success_url = reverse_lazy('core:admin_users')
    form_class = CustomUserCreationForm

    def form_valid(self, form) -> HTTPResponse:
        form.instance.role = 'client'
        form.instance.username = '{0}_{1}'.format(
            form.cleaned_data.get('username'),
            get_random_string(8)
        )
        # password = form.cleaned_data.get('password')
        # password2 = form.cleaned_data.get('password')

        # if password != password2:
        #     context = { 'error': 'passwords do not match'}
        #     return render(self.request, self.template_name, context)
            
        # user = form.save()
        # user.set_password(password)
        # user.save()
        return super().form_valid(form)


class AdminUserDelete(LoginRequiredMixin, DeleteView):
    model = User
    template_name = "core/admin_user_delete.html"
    success_url = reverse_lazy('core:admin_users')
    context_object_name = 'user'


class AdminUserDetail(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'core/admin_user_detail.html'
    context_object_name = 'user'



class AdminUpdateSolider(LoginRequiredMixin):
    pass


class AdminReplacementList(ListView):
    model = Replacement
    context_object_name = 'replacements'
    template_name = "core/admin_list_replacements.html"


class AdminRetirementList(ListView):
    model = Retirement
    context_object_name = 'retirements'
    template_name = "core/admin_list_retire.html"


class AdminGiftList(ListView):
    model = Gift
    context_object_name = 'gifts'
    template_name = "core/admin_list_gifts.html"


class AdminGiftDetail(DetailView):
    model = Gift
    context_object_name = 'gift'
    template_name = "core/admin_detail_gift.html"


# ---------------------------------------------------------
# ----------------- [User Section ] ---------------------  
# ---------------------------------------------------------

def user_logout(request):
    logout(request)
    return redirect('core:index')

class UserLogoutView(View):
    def get(self, *args, **kwargs):
        self.request.session.flush()
        return redirect('core:user_login')


def user_login(request):
    template_name = 'core/index.html'
    context = { "form": UserLoginForm() }

    if request.method == "POST":
        if not (login_form := UserLoginForm(request.POST)).is_valid():
            return render(request, template_name=template_name)

        try:
            # military_id  = request.POST.get('military_id', None)
            military_id  = request.POST.get('military_id', None)
            password  = request.POST.get('password', None)
            user_query =  User.objects.get(military_id=military_id)

            if not user_query.check_password(password):
                context = { 'error': 'Incorrect password' }
                return render(request, template_name, context)

            # if (user := authenticate(request, email=user_query.email, password=password)) is None:
            #     context = { 'error': 'Authentication Failed' }
            #     return render(request, template_name, context)


            # Assign user instance to session
            # login(request, user_query)
            user_obj = {
                'username': user_query.username,
                'id': str(user_query.pk),
                'pk': str(user_query.pk),
                'password': user_query.password,
                'first_name': user_query.first_name,
                'last_name': user_query.last_name,
                'military_id':  user_query.military_id,
                'zip_code':  user_query.zip_code,
                'image':  user_query.image.path,
                'country':  user_query.country.name,
                'gender':  user_query.gender,
                'email':  user_query.email,
            }
            request.session['user'] = user_obj
            return redirect('core:user_dashboard')

        except User.DoesNotExist as e:
            context = { 'error': 'No user with this details'}
            return render(request, template_name, context)
        
    return render(request, template_name, context)


class UserDashboard(TemplateView):
    template_name = 'core/user_dashboard.html'
    # model = User
    
    def get(self, *args, **kwargs):
        if not self.request.session.has_key('user'):
            return redirect('core:user_login')
        return super().get(self, *args, **kwargs)

    def get_context_data(self, **kwargs):
        cxt = super().get_context_data(**kwargs)
        cxt['user'] = self.request.session.get('user')
        return cxt



# ---------------------------------------
# ----------------[ User Retirement ] ---------
# ---------------------------------------

class UserRetirementView(ListView):
    model = Retirement
    template_name = 'core/user_retirement.html'
    context_object_name = 'retirements'


class UserRetirementCreationView(CreateView):
    model = Retirement
    template_name = "core/user_retirement_create.html"
    success_url = reverse_lazy('core:user_retirement_create')
    form_class = RetirementForm

    def form_valid(self, form) -> HttpResponse:
        user = self.request.session.get('user')
        form.instance.first_name = user.get('first_name')
        form.instance.last_name = user.get('last_name')
        form.instance.email = user.get('email')
        form.instance.zip_code = user.get('zip_code')
        form.instance.user = User.objects.get(pk=user.get('id'))
        form.save()
        return super().form_valid(form)

class UserRetirementDetailView(DetailView):
    model = Retirement
    context_object_name = 'application'
    template_name = 'core/user_retirement_detail.html'


# ---------------------------------------
# ----------------[ Replacement ] ---------
# ---------------------------------------

class UserReplacementView(ListView):
    model = Replacement
    template_name = 'core/user_replacement.html'
    context_object_name = 'replacements'


class UserReplacementCreateView(CreateView):
    model = Replacement
    template_name = 'core/user_replacement_create.html'
    success_url = reverse_lazy('core:user_replacement')
    form_class = ReplacementForm

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        user = self.request.session.get('user')
        form.instance.user  = User.objects.get(pk=user.get('id'))
        form.save()
        return super().form_valid(form)


class UserReplacementDetailView(DetailView):
    model = Retirement
    template_name = 'core/user_replacement_detail.html'


class UserTransferView(ListView):
    model = Retirement
    template_name = 'core/user_transfer.html'
    context_object_name = 'transfer'



# ---------------------------------------
# ----------------[ Gift Card ] ---------
# ---------------------------------------

class UserGiftListView(ListView):
    model = Gift
    template_name = 'core/user_gift.html'
    context_object_name = 'gift_cards'


class UserShareGiftView(CreateView):
    model = Gift
    template_name = 'core/user_gift_create.html'
    context_object_name = 'transfer'
    success_url = reverse_lazy('core:user_git_list')
    form_class = GiftCreationForm

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        try:
            user = self.request.session.get('user')
            form.instance.gift_card_to = User.objects.get(
                military_id=form.cleaned_data.get('solders_id_number')
            )
            form.instance.user  = User.objects.get(pk=user.get('id'))
            form.save()
        except User.DoesNotExist:
            return redirect('core:user_git_share')
        return super().form_valid(form)


class UserReplacementDetailView(DetailView):
    model = Gift
    template_name = 'core/user_gift_detail.html'
    context_object_name = "gift"


class UserSearchResult(View):
    template_name = 'core/user_search.html'

    def get(self, *args, **kwargs):
        context = {'user': ''}
        return render(self.request, self.template_name, context)

    def post(self, *args, **kwargs):
        try:
            if (search_params := self.request.POST.get('military_id', None)) is None:
                pass
            user = User.objects.get(military_id=search_params)
            return render(self.request, self.template_name, context={'user': user})
        except:
            return render(self.request, self.template_name, context={'user': None})
