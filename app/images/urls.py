from django.urls import path
from . import views

urlpatterns = [
    path('', views.ImagesApiOverview.as_view(), name='images'),
    path('image-list/', views.ImageListCreateAPIView.as_view(), name='list-create-image'),
    path('image-list/<int:pk>/', views.ImageDetailDestroyAPIView.as_view(), name='image-detail'),
    path('image-list/<int:pk>/expiring-link/', views.ExpiringLinkListCreateAPIView.as_view(), name='expiring-links'),
    path('image-list/thumbnails/', views.ThumbnailListApiView.as_view(), name='thumbnail-list'),
]