from django.urls import path
from . import views

urlpatterns = [
    path('', views.friends, name='friends'),
    path("update/<str:loaded_on>", views.update, name="update")
]
