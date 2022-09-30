from django.urls import path
from django.contrib.auth.views import  LogoutView

from .views import (
    UserDashboard,
    index,
    AdminDashboard,
    AdminLoginView,
    AdminUserList,
    AdminUserCreate,
    AdminUserDelete,
    AdminUserDetail,
    admin_logout,
    user_logout,
    user_login,
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
        'SC0gAo/admin/logout',
        admin_logout,
        name='admin_logout'
    ),

    # ------------------------------------------------------------
    # ----------------------- [ User Links ] ---------------------
    # ------------------------------------------------------------
    
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
]
