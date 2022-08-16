from django.urls import path
from . import views

urlpatterns = [
    path('user_profile/<int:user_id>/', views.see_user, name='user_profile'),
    path('home/', views.home, name='home'),
]