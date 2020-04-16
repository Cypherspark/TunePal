from django.db import models
from account.models import CustomUser as User
from django.utils.translation import ugettext_lazy as _

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

    def __str__(self):
        return "%s (%d): %s" % (
            self.sender_id.nickname, 
            self.conversation_id.id,
            self.text
        )