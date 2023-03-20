from django.urls import path

from . import views
from django.views.generic.base import RedirectView


urlpatterns = [
    path('', views.profile, name='profile'),
    path('<int:album_id>/', views.upload, name='upload'),
    path('<int:album_id>/upload/', views.upload, name='upload'),
    path('<int:album_id>/search/', views.search, name='search')
]