from django.contrib import admin

from .models import Event, EventCategory


class EventAdmin(admin.ModelAdmin):
    model = Event
    list_display = ("name", "status", "event_type", "start_date", "end_date")


admin.site.register(Event, EventAdmin)
admin.site.register(EventCategory)
