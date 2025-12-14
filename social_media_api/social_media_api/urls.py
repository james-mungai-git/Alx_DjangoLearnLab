from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse  # Add this import

# Create a simple root view
def root_view(request):
    return JsonResponse({
        'message': 'Welcome to Social Media API',
        'endpoints': {
            'accounts': {
                'register': '/api/accounts/register/',
                'login': '/api/accounts/login/',
                'profile': '/api/accounts/profile/',
                'logout': '/api/accounts/logout/',
            },
            'admin': '/admin/',
            'api_auth': '/api-auth/'
        }
    })

urlpatterns = [
    # Add this line - root path
    path('', root_view, name='root'),
    
    # Your existing patterns
    path('admin/', admin.site.urls),
    path('api/accounts/', include('accounts.urls')),
    path('api-auth/', include('rest_framework.urls')),
]

# Media files
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)