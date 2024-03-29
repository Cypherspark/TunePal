"""TunePal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from django.conf import settings
from django.conf.urls.static import static
from core.views import index



schema_view = get_schema_view(
    openapi.Info(
      title="Fuck API documentation",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    # path('asset-manifest.json', (TemplateView.as_view(template_name="asset-manifest.json",
    #                                                   content_type='application/manifest+json', )),
    #      name='asset-manifest.json'),
    # path('service-worker.js', (TemplateView.as_view(template_name="service-worker.js",
    #                                                 content_type='application/javascript', )),
    #      name='service-worker.js'),
    # path(precache_manifest_path, (
    #     TemplateView.as_view(template_name=precache_manifest_path,
    #                          content_type='application/javascript', )),
    #      name=precache_manifest_path),
    # path("", index, name="index"),
    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('api/admin/', admin.site.urls),
    path('api/account/', include('account.api.urls')),
    path('api/chat/', include('chat.api.urls')),
    path('api/spotify/', include('music.api.urls')),
    path('api/accounts/', include('rest_framework.urls')),
    path('api/quiz/', include('quiz.api.urls')),
    url(r'^.*/', index, name='base'),
    url(r'^$', index, name='base'),
    url(r'^(?:.*)/?$', index, name='base'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# if settings.DEBUG:
# urlpatterns += static(settings.MEDIA_URL,
#                               document_root=settings.MEDIA_ROOT)
