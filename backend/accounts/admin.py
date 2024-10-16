from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import Roles, Genders

# Register your models here.
User = get_user_model()


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "email",
        "mobile_no",
        "is_staff",
        "is_active",
        "created_at",
        "updated_at",
    )
    list_filter = ("is_staff", "is_active", "created_at", "updated_at")
    search_fields = ("email", "mobile_no")
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at")


admin.site.register(Roles)
admin.site.register(Genders)
