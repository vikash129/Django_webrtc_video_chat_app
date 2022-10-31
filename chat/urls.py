from django.urls import path , re_path
from . import views

    # re_path(r"ws/chat/(?P<room_name>\w+)/(?P<user_name>\w+)/(?P<choice>\w+)$", consumer.ChatConsumer.as_asgi()),

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    re_path(r"^chat/(?P<room_name>\w+)/(?P<created>\w+)/^(?P<name>)/(?P<id>\w+)$", views.room, name="room"),
] 
