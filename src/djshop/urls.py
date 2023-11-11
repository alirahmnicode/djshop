from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)


admin_urls = [
    path('api/admin/catalog/', include(('djshop.apps.catalog.urls.admin', 'djshop.apps.catalog'), namespace='catalog-admin'))
]

front_urls =[
    path('api/front/catalog/', include(('djshop.apps.catalog.urls.front', 'djshop.apps.catalog'), namespace='catalog-front'))
]


doc_patterns = [
    # YOUR PATTERNS
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

urlpatterns = [
    path("admin/", admin.site.urls),
] + front_urls + admin_urls + doc_patterns


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)