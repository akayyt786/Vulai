from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('apps.scans.urls')),
    # path('api/health/', views.health_check, name='health_check'), # To be added later
]
