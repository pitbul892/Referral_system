from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from api.views import RegisterWithReferralView

schema_view = get_schema_view(
    openapi.Info(
        title="Referral API",
        default_version='v1',
        description="API для реферальной системы",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('register/referral/',
         RegisterWithReferralView.as_view(),
         name='register_with_referral'
         )
]
