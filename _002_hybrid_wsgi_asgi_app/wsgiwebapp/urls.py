from django.urls import path
from django.contrib.auth.views import LoginView

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("other_view", views.other_view, name="other_view"),
    path("login", LoginView.as_view(template_name="login.html"), name="login"),
    path("auth", views.auth, name="auth")
]