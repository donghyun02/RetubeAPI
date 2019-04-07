from django.urls import path

from playlist import views

urlpatterns = [
    path('playlists/', views.PlaylistsView.as_view(), name="playlists"),
]