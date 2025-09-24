from django.urls import path
from . import views
app_name = 'Schools'
urlpatterns = [ 
    path('create/', views.create_school_view, name='create_school'),
    path('school_list/', views.school_list_view, name='school_list'),
    path('<str:school_name>/', views.school_detail_view, name='school_home'),
]