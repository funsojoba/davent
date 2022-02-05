from django.contrib import admin
from .models import Organization


class OrganizationAdmin(admin.ModelAdmin):
    model = Organization
    list_display = ("name", "owner", "category")


admin.site.register(Organization, OrganizationAdmin)
