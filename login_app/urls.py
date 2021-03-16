from django.urls import path
from . import views
urlpatterns = [
    path('', views.index),
    path('user/registration', views.user_registration),
    path('user/login', views.user_login),
    path('user/login/success/<int:user_id>', views.user_login_success),
    path('user/logout', views.user_logout),
]
