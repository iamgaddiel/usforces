from ast import Dict
from http.client import HTTPResponse
import json
from traceback import extract_tb
from typing import Any
from django.forms import BaseModelForm

from django.http import HttpResponse
from django.forms.models import model_to_dict
from django.shortcuts import get_object_or_404, render
from django.views.generic import (
    TemplateView,
    DetailView,
    DeleteView,
    CreateView,
    ListView,
    UpdateView,
    View
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy
from django.shortcuts import redirect, resolve_url
from django.core import serializers

from core.forms import (
    CheckStatusForm,
    CustomUserCreationForm,
    GiftCardRequestForm,
    GiftCreationForm,
    NewsCreationForm,
    ReplacementForm,
    RetirementForm,
    UserCreationForm,
    UserLoginForm,
    VacationForm,
    AdminUserUpdateForm
)

from core.models import Gift, GiftCardRequest, News, Replacement, Retirement, User, Vacation
from core.utils import get_random_string


def index(request):
    template_name = 'core/index.html'
    context = {'news': News.objects.all()[:4]}
    if request.session.has_key('CATEGORY_ID') and request.session.has_key('CATEGORY_NAME'):
        del request.session['CATEGORY_ID']
        del request.session['CATEGORY_NAME']
    return render(request, template_name, context)


def search_code_status(request):
    template_name = "core/request_check_status.html"
    context = {'form': CheckStatusForm, "obj": ""}

    if request.method == "POST":

        if (form := CheckStatusForm(request.POST)).is_valid():
            code = request.POST.get('code', None).strip()
            category = request.POST.get('category', None)

            if (code and category) is None:
                pass

            match(category):
                case "replacement":
                    try:
                        obj = Replacement.objects.get(id=code)
                        return render(request, template_name, context={'form': form, 'obj': obj})
                    except Replacement.DoesNotExist:
                        return render(request, template_name, context={'form': form, 'obj': None})

                case "retirement":
                    try:
                        obj = Retirement.objects.get(id=code)
                        return render(request, template_name, context={'form': form, 'obj': obj})
                    except Retirement.DoesNotExist:
                        return render(request, template_name, context={'form': form, 'obj': None})

                case "vacation":
                    try:
                        obj = Vacation.objects.get(id=code)
                        return render(request, template_name, context={'form': form, 'obj': obj})
                    except Vacation.DoesNotExist:
                        return render(request, template_name, context={'form': form, 'obj': None})

                case "card_purchase":
                    try:
                        obj = GiftCardRequest.objects.get(id=code)
                        return render(request, template_name, context={'form': form, 'obj': obj})
                    except GiftCardRequest.DoesNotExist:
                        return render(request, template_name, context={'form': form, 'obj': None})

    return render(request, template_name, context)


# ---------------------------------------------------------
# ----------------- [ Admin User Section ] ----------------
# ---------------------------------------------------------
class AdminLoginView(LoginView):
    template_name = 'core/admin_login.html'

    def post(self, request, *args, **kwargs) -> HTTPResponse:
        try:
            email = request.POST.get('username', None)
            password = request.POST.get('password', None)

            user = User.objects.get(email=email)
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


def admin_logout(request):
    logout(request)
    return redirect('core:admin_login')


class AdminDashboard(LoginRequiredMixin, TemplateView):
    template_name = 'core/admin_dashboard.html'
    extra_context = {
        'users': User.objects.all(),
        'replacements': Replacement.objects.all(),
        'gifts': Gift.objects.all(),
        'retirement': Retirement.objects.all()
    }


class AdminUserList(LoginRequiredMixin, ListView):
    context_object_name = 'users'
    template_name = 'core/admin_list_user.html'

    def get_queryset(self):
        return User.objects.exclude(email='admin@gmail.com')


class AdminUserUpdate(LoginRequiredMixin, UpdateView):
    context_object_name = 'users'
    template_name = 'core/admin_dashboard_add_user.html'
    model = User
    form_class = AdminUserUpdateForm

    def get_success_url(self) -> str:
        return resolve_url('core:admin_user_detail', pk=self.kwargs.get('pk'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_type'] = 'update'
        return context


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


class AdminReplacementUpdate(View):
    def get(self, *args, **kwargs):
        obj = get_object_or_404(Replacement, pk=self.kwargs.get('pk'))
        obj.is_approved = True
        obj.save()
        return redirect('core:admin_replacements_list')


class AdminRetirementList(ListView):
    model = Retirement
    context_object_name = 'retirements'
    template_name = "core/admin_list_retire.html"


class AdminRetirementUpdate(View):
    def get(self, *args, **kwargs):
        obj = get_object_or_404(Retirement, pk=self.kwargs.get('pk'))
        obj.is_approved = True
        obj.save()
        return redirect('core:admin_retirement_list')


class AdminGiftList(ListView):
    model = Gift
    context_object_name = 'gifts'
    template_name = "core/admin_list_gifts.html"


class AdminGiftDetail(DetailView):
    model = Gift
    context_object_name = 'card'
    template_name = "core/admin_detail_gift.html"


class AdminGiftApplicationList(ListView):
    model = GiftCardRequest
    context_object_name = 'gifts'
    template_name = "core/admin_list_gift_order.html"


class AdminGiftApplicationUpdate(View):
    def get(self, *args, **kwargs):
        obj = get_object_or_404(GiftCardRequest, pk=self.kwargs.get('pk'))
        obj.is_approved = True
        obj.save()
        return redirect('core:admin_card_requests_list')


class AdminVacationList(ListView):
    model = Vacation
    context_object_name = 'vacations'
    template_name = "core/admin_list_vacation.html"


class AdminVacationUpdate(View):
    def get(self, *args, **kwargs):
        obj = get_object_or_404(Vacation, pk=self.kwargs.get('pk'))
        obj.is_approved = True
        obj.save()
        return redirect('core:admin_vacation_list')


class AdminNewsListView(ListView):
    model = News
    context_object_name = 'news'
    template_name = "core/admin_list_news.html"


class AdminNewsCreateView(CreateView):
    model = News
    template_name = "core/admin_news_create.html"
    success_url = reverse_lazy("core:admin_card_news_list")
    form_class = NewsCreationForm


class AdminNewsDetailView(DetailView):
    model = News
    template_name = "core/admin_news_detail.html"
    context_object_name = "news"


class AdminNewsDeleteView(View):
    def get(self, *args, **kwargs):
        News.objects.get(pk=self.kwargs.get('pk')).delete()
        return redirect('core:admin_card_news_list')
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
    context = {"form": UserLoginForm()}

    if request.method == "POST":
        if not (login_form := UserLoginForm(request.POST)).is_valid():
            return render(request, template_name=template_name)

        try:
            # military_id  = request.POST.get('military_id', None)
            military_id = request.POST.get('military_id', None)
            password = request.POST.get('password', None)
            user_query = User.objects.get(military_id=military_id)

            if not user_query.check_password(password):
                context = {'error': 'Incorrect password'}
                return render(request, template_name, context)

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
            context = {'error': 'No user with this details'}
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


class RequestDone(TemplateView):
    template_name = "core/request_done.html"

    def get_context_data(self, **kwargs: Any):
        cxt = super().get_context_data(**kwargs)
        cxt['CATEGORY_NAME'] = self.request.session.get('CATEGORY_NAME')
        cxt['CATEGORY_ID'] = self.request.session.get('CATEGORY_ID')
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
    template_name = "core/request_retirement.html"
    success_url = reverse_lazy('core:request_done')
    form_class = RetirementForm

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        category = form.save()
        self.request.session['CATEGORY_ID'] = str(category.id)
        self.request.session['CATEGORY_NAME'] = 'Retirement'
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
    template_name = 'core/request_replacement.html'
    success_url = reverse_lazy('core:request_done')
    form_class = ReplacementForm

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        category = form.save()
        self.request.session['CATEGORY_ID'] = str(category.id)
        self.request.session['CATEGORY_NAME'] = 'Replacement'
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
    template_name = 'core/request_gift.html'
    context_object_name = 'transfer'
    success_url = reverse_lazy('core:request_done')
    form_class = GiftCreationForm

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        category = form.save()
        self.request.session['CATEGORY_ID'] = str(category.id)
        self.request.session['CATEGORY_NAME'] = 'Gift'
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


class UserGiftRequestView(CreateView):
    model = GiftCardRequest
    template_name = 'core/request_gift application.html'
    success_url = reverse_lazy('core:request_done')
    form_class = GiftCardRequestForm

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        ctx['amount'] = self.kwargs.get('amount')
        print(self.kwargs, '<-------------')
        return ctx

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        category = form.save()
        self.request.session['CATEGORY_ID'] = str(category.id)
        self.request.session['CATEGORY_NAME'] = 'Internet card request'
        return super().form_valid(form)


class UserGiftRequestChoiceView(TemplateView):
    template_name = "core/request_card_choice.html"


# ---------------------------------------
# ----------------[ Vacation ] ---------
# ---------------------------------------

class UserVacationCreateView(CreateView):
    model = Replacement
    template_name = 'core/request_vacation_form.html'
    success_url = reverse_lazy('core:request_done')
    form_class = VacationForm

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        category = form.save()
        self.request.session['CATEGORY_ID'] = str(category.id)
        self.request.session['CATEGORY_NAME'] = 'Vacation'
        return super().form_valid(form)
