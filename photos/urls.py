from django.urls import path

from . import views

urlpatterns = [
    path('<int:album_id>/', views.upload, name='upload'),
    path('<int:album_id>/upload/', views.upload, name='upload'),
    path('<int:album_id>/search/', views.search, name='search')
]