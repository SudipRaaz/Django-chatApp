from rest_framework import serializers
from .models import Message, Conversation
from usermanagement.models import MyUser

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'

class ConversationSerializer(serializers.ModelSerializer):
    participant_ids = serializers.ListField(
        child=serializers.IntegerField(), write_only=True
    )

    class Meta:
        model = Conversation
        fields = ['id', 'participant_ids', 'created_at', 'updated_at']

    def create(self, validated_data):
        participant_ids = validated_data.pop('participant_ids', [])
        participants = MyUser.objects.filter(id__in=participant_ids)
        conversation = Conversation.objects.create(**validated_data)
        conversation.participants.set(participants)
        return conversation
    
    
# serializers.py
class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'conversation', 'sender', 'content', 'timestamp', 'is_read']
        read_only_fields = ['id', 'conversation', 'sender', 'timestamp', 'is_read']

    def create(self, validated_data):
        message = Message.objects.create(**validated_data)
        return message