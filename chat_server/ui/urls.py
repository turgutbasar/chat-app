from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('room', views.room, name='room'),
    path('message_listener', views.message_listener, name='message_listener'),
    path('message_send', views.message_send, name='message_send'),
]
