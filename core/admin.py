from django.contrib import admin
from .models import (
    User,
    Retirement, 
    GiftCardRequest,
    Vacation,
    News,
    Gift,
    Replacement,
    Operations,
)

# Register your models here.
admin.site.register(User)
admin.site.register(Retirement)
admin.site.register(GiftCardRequest)
admin.site.register(Vacation)
admin.site.register(News)
admin.site.register(Gift)
admin.site.register(Replacement)
admin.site.register(Operations)
