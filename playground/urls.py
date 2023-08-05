from . import views
from django.urls import path

urlpatterns = [
    path('products/',views.say_hello)
]
