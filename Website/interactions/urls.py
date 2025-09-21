from django.urls import path
from . import views

app_name = "interactions"

urlpatterns = [
    path("inbox/", views.inbox_view, name="inbox"),
    path("outbox/", views.outbox_view, name="outbox"),
    path("compose/", views.compose_view, name="compose"),
    path("<int:pk>/", views.message_detail_view, name="detail"),
]
