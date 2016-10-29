from django.db import models as m
from django.contrib.auth.models import User


# Create your models here.

class SellerAccount(m.Model):
    user = m.ForeignKey(User)
    managers = m.ManyToManyField(User, related_name='manager_sellers', blank=True)
    # we want the seller accounts to be manually approved
    active = m.BooleanField(default=False)
    timestamp = m.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self):
        return self.user.username


