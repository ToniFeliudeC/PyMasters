"""PruebaProyecto URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path
from PruebaProyectoApp.views import retos, crea_challenge, log_in, reto, log_out, challenges_reviews

# Para los static
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', retos, name='retos'),
    path('accounts/login/', log_in, name='login'),
    # path("register", register_request, name="register"),
    path('logout/', log_out, name='logout'),
    path('admin/', admin.site.urls),
    path('retos/', retos, name='retos'),
    path('retos/<int:reto_id>/', reto, name='reto'),
    path('crea_challenges/', crea_challenge, name='crea_challenges'),
    path('challenge_reviews/', challenges_reviews, name='challenges_reviews')
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
