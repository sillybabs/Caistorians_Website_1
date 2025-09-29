

from django.urls import path
from . import views

app_name = "notifications"

urlpatterns = [
    path("", views.notifications_list, name="list"),
    path("read/<int:pk>/", views.mark_as_read, name="mark_as_read"),  # ✅ delete on read
]
