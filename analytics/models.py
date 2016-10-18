from django.contrib.auth.models import User
from django.db import models as m

from tags.models import Tag


class TagViewManager(m.Manager):
    def add_count(self, user, tag):

        obj = self.model.objects.get_or_create(
            user=user,
            tag=tag)[0]

        obj.count += 1
        obj.save()
        return obj


# def is_active(instance):
#     if instance.tag.active:
#         is_active = True
#     else:
#         is_active = False
#     return is_active

def is_active(instance):
    if instance.tag.active:
       active = True
    else:
        active = False
    return active


class TagView(m.Model):

    user = m.ForeignKey(User, blank=True, null=True)
    tag = m.ForeignKey(Tag)
    count = m.IntegerField(default=0)
    is_active = m.BooleanField(default=True)

    objects = TagViewManager()

    def __str__(self):
        return '{}: {} - {} times'.format(
            str(self.tag.title).upper(),
            str(self.user).capitalize(),
            self.count)


