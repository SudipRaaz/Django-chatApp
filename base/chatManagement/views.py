# views.py
from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Conversation, Message, Media
from .serializers import ConversationSerializer, MessageSerializer, MediaSerializer
# from usermanagement.models import MyUser
from rest_framework.exceptions import PermissionDenied
from rest_framework.parsers import MultiPartParser, FormParser

# The `ConversationViewSet` class defines view methods for handling conversations with participants
# filtered by the current user.
class ConversationViewSet(viewsets.ModelViewSet):
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Conversation.objects.filter(participants=self.request.user)

    def create(self, request, *args, **kwargs):
        participant_ids = request.data.get('participant_ids', [])
        if not participant_ids:
            return Response({"detail": "Participant IDs are required."}, status=400)
        # add a validation to not add active user's participant id

        # Include the current user if not already included
        if request.user.id not in participant_ids:
            participant_ids.append(request.user.id)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        conversation = serializer.save(participant_ids=participant_ids)
        
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=201, headers=headers)

class MessageListCreateView(generics.ListCreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        conversation_id = self.kwargs['conversation_id']
        return Message.objects.filter(conversation_id=conversation_id)

    def perform_create(self, serializer):
        conversation_id = self.kwargs['conversation_id']
        conversation = Conversation.objects.get(id=conversation_id)
        serializer.save(conversation=conversation, sender=self.request.user)

    def delete(self, request, *args, **kwargs):
        message_id = self.kwargs['pk']
        message = Message.objects.get(id=message_id)

        # Check if the authenticated user is the sender of the message
        if message.sender != request.user:
            raise PermissionDenied("You do not have permission to delete this message.")

        # Delete the message
        message.delete()
        return Response({"status_code":204, "message":"Message deleted successfully"})

class ConversationMessagesView(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        conversation_id = self.kwargs['conversation_id']
        return Message.objects.filter(conversation_id=conversation_id)

class MediaUploadView(generics.CreateAPIView):
    serializer_class = MediaSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        conversation_id = self.kwargs['conversation_id']
        conversation = Conversation.objects.get(id=conversation_id)
        serializer.save(conversation=conversation, sender=self.request.user)

class MediaListView(generics.ListAPIView):
    serializer_class = MediaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        conversation_id = self.kwargs['conversation_id']
        return Media.objects.filter(conversation_id=conversation_id)