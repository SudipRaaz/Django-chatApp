# models.py
<<<<<<< HEAD
=======
from django.conf import settings
>>>>>>> workingdir
from django.db import models
from usermanagement.models import MyUser

class Conversation(models.Model):
    participants = models.ManyToManyField(MyUser, related_name='user_conversations')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Conversation {self.id}'

class Message(models.Model):
    conversation = models.ForeignKey(Conversation, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(MyUser, related_name='messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f'Message {self.id} from {self.sender}'

class Participant(models.Model):
    conversation = models.ForeignKey(Conversation, related_name='conversation_participants', on_delete=models.CASCADE)
    user = models.ForeignKey(MyUser, related_name='user_participants', on_delete=models.CASCADE)
    last_read_message = models.ForeignKey(Message, related_name='+', null=True, blank=True, on_delete=models.SET_NULL)
    joined_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} in conversation {self.conversation.id}'
<<<<<<< HEAD
=======


class Media(models.Model):
    file = models.FileField(upload_to='chat_media/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    conversation = models.ForeignKey('Conversation', related_name='media', on_delete=models.CASCADE)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sent_media', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.file.name} uploaded by {self.sender}'
>>>>>>> workingdir
