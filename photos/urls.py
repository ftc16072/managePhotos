from django.urls import path

from . import views
from django.views.generic.base import RedirectView

urlpatterns = [
    path('', views.profile, name='profile'),
    path('admin/<int:team_id>/', views.team_admin, name='team_admin'),
    path('admin/<int:team_id>/promote/<int:user_id>/',
         views.team_promote,
         name='team_promote'),
    path('admin/<int:team_id>/demote/<int:user_id>/',
         views.team_demote,
         name='team_demote'),
    path('admin/<int:team_id>/remove/<int:user_id>/',
         views.team_remove,
         name='team_remove'),
    path('<int:album_id>/', views.upload, name='upload'),
    path('<int:album_id>/upload/', views.upload, name='upload'),
    path('<int:album_id>/search/', views.search, name='search'),
    path('<int:album_id>/sync/', views.sync, name='sync'),
    path('<int:album_id>/edit/<int:photo_id>/', views.edit, name='edit')
]