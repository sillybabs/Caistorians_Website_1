from django.urls import path
from . import views
app_name = 'Main'
urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('site_home/', views.site_home, name='site_home'),
]