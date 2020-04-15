from django.db import models
from account.models import CustomUser as User
from django.utils.translation import ugettext_lazy as _

# Create your models here.


class Conversation(models.Model):
    name = models.CharField(max_length=100)
    members = models.ManyToManyField(Users)
    is_group = models.BooleanField(_("is_group"),default=False)

    def __str__(self):
        return self.name


class Message(models.Model):
    sender_id = models.ForeignKey(
        User,
        on_delete=models.CASCADE)
    conversation_id = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE
    )
    text = models.TextField()
    date = models.DateField()
    is_seen = models.BooleanField(_("is_seen"),default=False)

    def __str__(self):
        return "%s (%s): %s" % (
            self.sender_id.first_name, 
            self.conversation_id.name,
            self.text
        )