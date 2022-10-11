from django.urls import path
from django.contrib.auth.views import  LogoutView

from core.models import GiftCardRequest

from .views import (
    AdminGiftApplicationList,
    AdminGiftApplicationUpdate,
    AdminGiftDetail,
    AdminGiftList,
    AdminReplacementList,
    AdminReplacementUpdate,
    AdminRetirementList,
    AdminRetirementUpdate,
    AdminVacationList,
    AdminVacationUpdate,
    RequestDone,
    UserDashboard,
    UserGiftListView,
    UserGiftRequestView,
    UserReplacementCreateView,
    UserReplacementDetailView,
    UserRetirementCreationView,
    UserRetirementDetailView,
    UserSearchResult,
    UserShareGiftView,
    UserTransferView,
    UserVacationCreateView,
    index,
    AdminDashboard,
    AdminLoginView,
    AdminUserList,
    AdminUserCreate,
    AdminUserDelete,
    AdminUserDetail,
    admin_logout,
    search_code_status,
    user_logout,
    user_login,
    UserLogoutView,
    UserRetirementView,
    UserReplacementView,
)


app_name = 'core'

urlpatterns = [
    path('', index, name='index'),
    path(
        'SC0gAo/admin/login',
        AdminLoginView.as_view(),
        name='admin_login'
    ),
    path(
        'SC0gAo/admin/dashboard',
        AdminDashboard.as_view(),
        name='admin_dashboard'
    ),
    path(
        'SC0gAo/admin/users',
        AdminUserList.as_view(),
        name='admin_users'
    ),
    path(
        'SC0gAo/admin/user/add',
        AdminUserCreate.as_view(),
        name='admin_user_create'
    ),
    path(
        'SC0gAo/admin/user/remove/<uuid:pk>/',
        AdminUserDelete.as_view(),
        name='admin_user_delete'
    ),
    path(
        'SC0gAo/admin/user/<uuid:pk>/',
        AdminUserDetail.as_view(),
        name='admin_user_detail'
    ),
    path(
        'SC0gAo/admin/replacements/',
        AdminReplacementList.as_view(),
        name='admin_replacements_list'
    ),
    path(
        'SC0gAo/admin/replacements/<uuid:pk>/',
        AdminReplacementUpdate.as_view(),
        name='admin_replacements_update'
    ),
    path(
        'SC0gAo/admin/retirements/',
        AdminRetirementList.as_view(),
        name='admin_retirement_list'
    ),
    path(
        'SC0gAo/admin/retirement/<uuid:pk>/',
        AdminRetirementUpdate.as_view(),
        name='admin_retirement_update'
    ),
    path(
        'SC0gAo/admin/gifts/',
        AdminGiftList.as_view(),
        name='admin_gift_list'
    ),
    path(
        'SC0gAo/admin/gift/<uuid:pk>/',
        AdminGiftDetail.as_view(),
        name='admin_gift_detail'
    ),
    path(
        'SC0gAo/admin/logout',
        admin_logout,
        name='admin_logout'
    ),
    path(
        'SC0gAo/admin/vacation/list',
        AdminVacationList.as_view(),
        name='admin_vacation_list'
    ),
    path(
        'SC0gAo/admin/vacation/<uuid:pk>/',
        AdminVacationUpdate.as_view(),
        name='admin_vacation_update'
    ),
    path(
        'SC0gAo/admin/card/requests/',
        AdminGiftApplicationList.as_view(),
        name='admin_card_requests_list'
    ),
    path(
        'SC0gAo/admin/card/requests/<uuid:pk>/',
        AdminGiftApplicationUpdate.as_view(),
        name='admin_card_requests_update'
    ),

    # -----------------------------------------
    # -----[ User Links ] ---------------------
    # -----------------------------------------
    
    path(
        'login/',
        user_login,
        name='user_login'
    ),
    path(
        'logout/',
        user_logout,
        name='user_logout'
    ),
    path(
        'dashboard/',
        UserDashboard.as_view(),
        name='user_dashboard'
    ),
    path(
        'logout',
        UserLogoutView.as_view(),
        name='user_logout'
    ),
    # ---------------------------------------
    # ----------------[ Retirement ] --------
    # ---------------------------------------
    path(
        'retirement',
        UserRetirementView.as_view(),
        name='user_retirement'
    ),
    path(
        'retirement/create/',
        UserRetirementCreationView.as_view(),
        name='user_retirement_create'
    ),
    path(
        'retirement/detail/<uuid:pk>/',
        UserRetirementDetailView.as_view(),
        name='user_retirement_detail'
    ),
    # ---------------------------------------
    # ----------------[ Replacement ] -------
    # ---------------------------------------
    path(
        'replacement',
        UserReplacementView.as_view(),
        name='user_replacement'
    ),
    path(
        'replacement/create/',
        UserReplacementCreateView.as_view(),
        name='user_replacement_create'
    ),
    path(
        'replacement/detail/<uuid:pk>/',
        UserReplacementDetailView.as_view(),
        name='user_replacement_detail'
    ),
    # ---------------------------------------
    # ----------------[ Transfer ] ----------
    # ---------------------------------------
    path(
        'transfer',
        UserTransferView.as_view(),
        name='user_transfer'
    ),

    # ---------------------------------------
    # ----------------[ Gift Card ] ---------
    # ---------------------------------------
    path(
        'gift/list/',
        UserGiftListView.as_view(),
        name='user_git_list'
    ),
    path(
        'gift/share/',
        UserShareGiftView.as_view(),
        name='user_git_share'
    ),
    path(
        'gift/detail/<uuid:pk>?',
        UserReplacementDetailView.as_view(),
        name='user_git_detail'
    ),
    path(
        'search/',
        UserSearchResult.as_view(),
        name='user_search'
    ),
    path(
        'request/done/',
        RequestDone.as_view(),
        name='request_done'
    ),
    path(
        'request/check/',
        search_code_status,
        name='request_check'
    ),
    path(
        'request/vacation/',
        UserVacationCreateView.as_view(),
        name='request_vacation'
    ),
    path(
        'request/card/order/',
        UserGiftRequestView.as_view(),
        name='request_card_order'
    ),
]
