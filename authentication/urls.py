from django.urls import path
from authentication import views

urlpatterns = [
    path('', views.login_page, name='login'),
    path('signup/', views.signup_page, name='signup'),
    path('logout/', views.logout_user, name='logout'),
]