"""YaMDb URL Configuration.

Contains:
- Category endpoints (/categories/)
- Genre endpoints (/genres/)
- Title endpoints (/titles/)
- User endpoints (/users/)
- Review endpoints (/titles/{title_id}/reviews/)
- Comment endpoints (/titles/{title_id}/reviews/{review_id}/comments/)
- Auth endpoints (/auth/signup/, /auth/token/)
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView


urlpatterns = [
    path('admin/', admin.site.urls),
    path(
        'redoc/',
        TemplateView.as_view(template_name='redoc.html'),
        name='redoc'
    ),
    path('api/', include('api.urls')),
]
