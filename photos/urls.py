from django.urls import path

from . import views
from django.views.generic.base import RedirectView

urlpatterns = [
    path('', views.profile, name='profile'),
    path('admin/<int:team_id>/', views.team_admin, name='team_admin'),
    path('<int:album_id>/', views.upload, name='upload'),
    path('<int:album_id>/upload/', views.upload, name='upload'),
    path('<int:album_id>/search/', views.search, name='search'),
    path('<int:album_id>/sync/', views.sync, name='sync'),
    path('<int:album_id>/edit/<int:photo_id>/', views.edit, name='edit')
]