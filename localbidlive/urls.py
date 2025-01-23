"""
URL configuration for localbidlive project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.views.i18n import set_language

# Non-translatable URLs
urlpatterns = [
    path('i18n/setlang/', set_language, name='set_language'),
]

# Translatable URLs
urlpatterns += i18n_patterns(
    path("admin/", admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('rosetta/', include('rosetta.urls')),
    path('accounts/', include('accounts.urls')),
    path('auctions/', include('auctions.urls')),
    path('notifications/', include('notifications.urls')),
    prefix_default_language=False
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
