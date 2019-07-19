from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from django.urls import include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.homepage),
    path('info/', views.info, name='info'),
    path('state/', views.state, name='state'),
    path('take_picture/', views.take_picture, name='take_picture'),
    path('image_urls/', views.image_urls, name='image_urls'),
    path('download_image/', views.download_image, name='download_image'),
    path('download_all_images/', views.download_all_images, name='download_all_images'),





] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
