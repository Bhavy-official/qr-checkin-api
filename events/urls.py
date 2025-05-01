from django.urls import path
from .views import EventCreateView, EventListView, EventRegistrationView, EventRegistrationListView, CheckInView, CheckInExportView, EventCheckInSummaryView

urlpatterns = [
    path('create/', EventCreateView.as_view(), name='create_event'),
    path('list/', EventListView.as_view(), name='list-events'),
    path('register/', EventRegistrationView.as_view(), name='event-register'),
    path('register/<int:event_id>/', EventRegistrationListView.as_view(), name='event-registration-list'), 
    path('checkin/', CheckInView.as_view(), name='checkin'),
    path('checkins/export/', CheckInExportView.as_view(), name='checkin-export'),
    path('<int:event_id>/checkin/summary/', EventCheckInSummaryView.as_view(), name='checkin-summary'),
]
