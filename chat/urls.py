from django.urls import path
from . import views

app_name = "chat"

# urls.py
urlpatterns = [
    path('chatchat/<int:year_group>/', views.year_group_chat, name='year_group_chat'),
    path('chatchat/', views.redirect_chat, name="chat_redirect"),
]
