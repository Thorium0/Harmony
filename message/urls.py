from django.urls import path
from . import views

urlpatterns = [
    path("add/", views.add_friend, name="add_friend"),
    path("finalize/<id>", views.finalize_friend, name="finalize_friend"),
    path("remove_request/<id>", views.remove_request, name="remove_friend_request")
]
