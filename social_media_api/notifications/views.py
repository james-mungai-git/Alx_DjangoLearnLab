from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import Notification


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def list_notifications(request):
    """
    Fetch all notifications for the logged-in user.
    Unread notifications are shown first.
    """
    notifications = Notification.objects.filter(recipient=request.user).order_by("read", "-timestamp")

    data = []
    for n in notifications:
        data.append({
            "id": n.id,
            "actor": n.actor.username,
            "verb": n.verb,
            "target": str(n.target) if n.target else None,
            "timestamp": n.timestamp,
            "read": n.read,
        })

    return Response(data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def mark_notification_read(request, notification_id):
    """
    Mark a specific notification as read.
    """
    notification = get_object_or_404(Notification, id=notification_id, recipient=request.user)
    notification.read = True
    notification.save()
    return Response({"detail": "Notification marked as read."})