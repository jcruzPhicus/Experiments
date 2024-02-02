from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("other_view", views.other_view, name="other_view"),
]