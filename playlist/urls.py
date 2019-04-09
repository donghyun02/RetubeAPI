from django.urls import path

from playlist import views

urlpatterns = [
    path('playlists/', views.PlaylistsView.as_view(), name="playlists"),
    path('playlist/<int:playlist_id>/', views.PlaylistView.as_view(), name="playlist"),
]