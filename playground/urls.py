from django.urls import path
from . import views #curent folder import view

urlpatterns = [
    path('hello/',views.say_hello)
]