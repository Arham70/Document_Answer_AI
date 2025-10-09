from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('', views.chat_list, name='chat_list'),
    path('<uuid:chat_id>/', views.chat_detail, name='chat_detail'),
    path('start/<uuid:document_id>/', views.start_chat, name='start_chat'),
    path('<uuid:chat_id>/send/', views.send_message, name='send_message'),
    path('<uuid:chat_id>/export/', views.export_chat, name='export_chat'),
]
