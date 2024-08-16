# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ConversationViewSet, MessageListCreateView, ConversationMessagesView, MediaUploadView, MediaListView

router = DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')

urlpatterns = [
    path('', include(router.urls)),
    path('conversations/<int:conversation_id>/messages/', MessageListCreateView.as_view(), name='message-list-create'),
    path('messages/<int:pk>/', MessageListCreateView.as_view(), name='message-delete'),
    path('conversations/<int:conversation_id>/messages/list/', ConversationMessagesView.as_view(), name='conversation-messages'),

    path('conversations/<int:conversation_id>/media/', MediaListView.as_view(), name='media-list'),
    path('conversations/<int:conversation_id>/media/upload/', MediaUploadView.as_view(), name='media-upload'),

]