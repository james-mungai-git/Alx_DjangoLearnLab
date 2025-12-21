from django.urls import path
from . import views
from .views import list_notifications, mark_notification_read

urlpatterns = [
    path('notifications/', views.list_notifications, name='list-notifications'),
    path('read-notifications/<int:notification_id>/read/', views.mark_notification_read, name='read-notifications')
]