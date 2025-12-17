from django.contrib import admin
from django.urls import path, include  # include is needed to link app URLs

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')), 
]
