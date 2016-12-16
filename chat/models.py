from __future__ import unicode_literals

from django.db import models
from django.utils import timezone


class Room(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class History(models.Model):
    room = models.ForeignKey(Room, related_name='history')

    username = models.CharField(max_length=30)
    datetime = models.DateTimeField(default=timezone.now, db_index=True)
    message = models.TextField()

    @property
    def formatted_timestamp(self):
        return self.datetime.strftime('%b %-d %-I:%M %p')

    def as_dict(self):
        return {'username': self.username, 'message': self.message, 'datetime': self.formatted_timestamp}
