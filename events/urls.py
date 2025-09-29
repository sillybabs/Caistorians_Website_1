# events/urls.py
from django.urls import path
from . import views

app_name = "events"

urlpatterns = [
    path("", views.event_list_view, name="event_list"),
    path("<int:pk>/", views.event_detail_view, name="event_detail"),
    path("create/", views.event_create, name="create_event"),
    path("<int:pk>/edit/", views.event_update, name="event_update"),
    path("<int:pk>/delete/", views.event_delete, name="event_delete"),
    path("<int:pk>/rsvp/", views.rsvp_event, name="event_rsvp"),
]