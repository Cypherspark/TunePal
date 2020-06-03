from django.db import models
from account.models import CustomUser as User
from django.utils.translation import ugettext_lazy as _

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


# Create your models here.


class Conversation(models.Model):
    name = models.CharField(max_length=100,blank=True,null =True)
    members = models.ManyToManyField(User)
    is_group = models.BooleanField(_("is_group"),default=False)

    def __str__(self):
        return f"{self.id}"


class Message(models.Model):
    sender_id = models.ForeignKey(
        User,
        on_delete=models.CASCADE)
    conversation_id = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE
    )
    text = models.TextField()
    date = models.DateTimeField(_("time"), auto_now=False, auto_now_add=False)
    is_seen = models.BooleanField(_("is_seen"),default=False)

    def notify_ws_clients(self):
        """
        Inform client there is a new message.
        """
        notification = {
            'type': 'chat_message',
            'message': '{}'.format(self.id), 
            'text': self.text, 
            'conversation_id': self.conversation_id          
        }

        channel_layer = get_channel_layer()
        # print("user.id {}".format(self.sender_id.id))
        # print("user.id {}".format(self.conversation_id.id))

        async_to_sync(channel_layer.group_send)("{}".format(self.sender_id.id), notification)
        for person in self.conversation_id.members.exclude(id = self.user.id).values_list('id', flat=True):
            print("person: " ,person)
            async_to_sync(channel_layer.group_send)("{}".format(self.person), notification)

    def save(self, *args, **kwargs):
        """
        Trims white spaces, saves the message and notifies the recipient via WS
        if the message is new.
        """
        new = self.id
        self.text = self.text.strip()  # Trimming whitespaces from the body
        super(Message, self).save(*args, **kwargs)
        if new is None:
            self.notify_ws_clients()


    def __str__(self):
        return "%s (%d): %s" % (
            self.sender_id.nickname, 
            self.conversation_id.id,
            self.text
        )