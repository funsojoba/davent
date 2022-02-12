from django.contrib import admin

from authentication.models import User


class UserAdmin(admin.ModelAdmin):
    model = User
    list_display = ("first_name", "last_name", "email", "created_at")
    ordering = ("-created_at",)

    # def has_change_permission(self, request, obj=None):
    #     return False


admin.site.register(User, UserAdmin)
