from django.urls import path
from . import views

app_name = 'diagnostic'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('', views.index, name='index'),
    path('predict/', views.predict, name='predict'),
    path('history/', views.history, name='history'),
]