from django.urls import path
from . import views

urlpatterns = [
    path("friend/add/", views.add_friend, name="add_friend"),
    path("friend/finalize/<id>", views.finalize_friend, name="finalize_friend"),
    path("friend/remove_request/<id>", views.remove_request, name="remove_friend_request"),
    path("", views.servers, name="servers"),
    path("server/<server_name>", views.server_select, name="server_select"),
    path("server/join", views.join_server, name="join_server"),
    path("server/update/<str:loaded_on>/<int:server_id>", views.server_update, name="server_update")

]
