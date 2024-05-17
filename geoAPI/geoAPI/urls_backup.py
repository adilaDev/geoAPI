# =============================================================================
# Original code by Django
# =============================================================================
"""geoAPI URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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

urlpatterns = [
    path('admin/', admin.site.urls),
]
# =============================================================================
# Original code by Django
# =============================================================================

# =============================================================================
# Change code by Fadil
# =============================================================================
from django.conf.urls import url
from django.urls import path
from django.contrib import admin
from . import views
from . import api

urlpatterns = [
    path('', views.get_data, name='root'),
    path('admin/', admin.site.urls),
    path('<nama_folder>/<nama_file>/', views.get_data, name='get_data'),
]

# urlpatterns = [
#     url(r'^admin/', admin.site.urls),
#     url(r'^(?P<nama_folder>\w+)/(?P<nama_file>\w+)/$', views.get_data, name='get_data'),
# ]
# =============================================================================
# Change code by Fadil
# =============================================================================


