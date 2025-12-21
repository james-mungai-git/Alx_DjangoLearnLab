from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey



# Create your models here.
class Notification(models.Model):
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notifications")
    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications_sent"
    )
    verb = models.CharField(max_length=255)  # e.g. "liked", "commented", "followed"

    # Generic relation to any object (Post, Comment, etc.)
    target_content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    target_object_id = models.PositiveIntegerField(blank=True, null=True)
    target = GenericForeignKey("target_content_type", "target_object_id")

    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    class Meta:
        ordering = ["-timestamp"]

    def __str__(self):
        if self.target:
            return f"{self.actor} {self.verb} {self.target} for {self.recipient}"
        return f"{self.actor} {self.verb} for {self.recipient}"
