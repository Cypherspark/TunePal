from django.db import models
from account.models import CustomUser as User
from django.utils.translation import ugettext_lazy as _

# Create your models here.


class Conversation(models.Model):
    name = models.CharField(max_length=100,blank=True,null =True)
    members = models.ManyToManyField(User)
    is_group = models.BooleanField(_("is_group"),default=False)
    admin = models.ManyToManyField(User,blank = True, related_name = "admin")
    pin_message = models.TextField()



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
#
# class Admin(models.Model):
#     admin = models.ManyToManyField(User)
# class Group(models.Model):
#     group_name = models.CharField(max_length = 200)
#     admin = models.ManyToManyField(Admin)
#     members = models.ManyToManyField(User,default = None,blank = True)
#
#     def __str__(self):
#         return f"{self.id}"
#
# class GroupMessage(models.Model):
#     sender_id = models.ForeignKey(
#         User,
#         on_delete=models.CASCADE)
#     conversation_id = models.ForeignKey(
#         Group,
#         on_delete=models.CASCADE
#     )
#     text = models.TextField()
#     # date = models.DateTimeField(("time"), auto_now=False, auto_now_add=False)
#     # is_seen = models.BooleanField(("is_seen"),default=False)
#
#     def __str__(self):
#         return "%s (%d): %s" % (
#             self.sender_id.nickname,
#             self.conversation_id.id,
#             self.text
#         )
