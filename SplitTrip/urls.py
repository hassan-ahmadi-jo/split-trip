"""
URL configuration for SplitTrip project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns

urlpatterns = []

urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),

    # --- Public Website
    path('', include('core.urls')),

    # --- App
    path('apps/splitter/', include('events.urls.web_urls')),
    path('apps/splitter/events/<str:event_code>/tracker/', include('expenses.urls')),

    # --- API
    path('api/events/', include('events.urls.api_urls')),

    # --- Accounts
    path('accounts/', include('accounts.urls')),

    # DRF auth
    path('api-auth/', include('rest_framework.urls')),

    # ROSETTA
    path('rosetta/', include('rosetta.urls'))
)


