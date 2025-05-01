from django.contrib import admin
from .models import User
from events.models import Event, EventRegistration, CheckIn


admin.site.register(User)
admin.site.register(Event)
admin.site.register(EventRegistration)
admin.site.register(CheckIn)
