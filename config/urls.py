
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from dashboard import views as dashboard_views


urlpatterns = [
    # Django's built-in administration site.
    # Keep this route for internal maintenance.
    path("admin/", admin.site.urls),

    # Public website.
    path("", dashboard_views.public_home, name="public_home"),
    # Main dashboard.
path("dashboard/", include("dashboard.urls")),
    # Authentication and accounts.
    path("accounts/", include("accounts.urls")),

    # Citizen portal.
    path("citizen/", include("citizen.urls")),

    # City Admin portal.
    path("city-admin/", include("city_admin.urls")),

    # Government services.
    path("services/", include("services.urls")),
    path("health/", include("health.urls")),
    path("education/", include("education.urls")),
    path("agriculture/", include("agriculture.urls")),
    path("water/", include("water.urls")),
    path("public-works/", include("public_works.urls")),
    path("energy/", include("energy.urls")),
    path("security/", include("security.urls")),
    

    # Employment, payments and reports.
    path("jobs/", include("jobs.urls")),
   
    path("reports/", include("reports.urls")),

    # Requests and communication.
    path("requests/", include("requests.urls")),
    path("notifications/", include("notifications.urls")),
    path("lands/", include("lands.urls")),

    # Staff portals.
    path("officer/", include("officer.urls")),
    path("calendar/", include("calendar_app.urls")),
  

    # Department and location management.
    path("departments/", include("departments.urls")),
    path("locations/", include("locations.urls")),
]


# Serve uploaded media files during local development only.
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
