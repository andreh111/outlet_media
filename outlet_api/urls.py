from django.urls import path, include
from outlet_api.views import account, settings, outlet

urlpatterns = [
    path('account/', include(account.urls)),
    path('settings/', include(settings.urls)),
    path('outlet/', include(outlet.urls)),
]
