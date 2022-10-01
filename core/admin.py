from django.contrib import admin
from .models import (
    User,
    Retirement,
)

# Register your models here.
admin.site.register(User)
admin.site.register(Retirement)
