from django.contrib import admin

from core.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "first_name", "last_name")
    exclude = ("password",)
    readonly_fields = ("date_joined", "last_login")
    list_filter = ("is_staff", "is_active", "is_superuser")
    search_fields = ("emailfirst_name", "last_name", "username")
