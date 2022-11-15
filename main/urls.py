from django.urls import path
from . import views

urlpatterns = [
    path('', views.friends, name='friends'),
    path('<int:user_id>', views.friend_select, name='friend_select'),
    path("update/<str:loaded_on>/<int:user_id>", views.update, name="update"),
    path("call/<int:user_id>", views.call, name="call")
]
