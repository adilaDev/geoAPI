from django.urls import path
from django.contrib import admin
from . import views

urlpatterns = [
    path('', views.get_data, name='root'),
    path('admin/', admin.site.urls),
    path('<nama_folder>/<nama_file>/', views.get_data, name='get_data'),
]
