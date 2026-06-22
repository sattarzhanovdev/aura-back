from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/", include("apps.accounts.urls")),
    path("api/onboarding/", include("apps.accounts.onboarding_urls")),
    path("api/wardrobe/", include("apps.wardrobe.urls")),
    path("api/weather/", include("apps.weather.urls")),
    path("api/outfits/", include("apps.outfits.urls")),
    path("api/generation/", include("apps.generation.urls")),
    path("api/callback/", include("apps.generation.callback_urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
