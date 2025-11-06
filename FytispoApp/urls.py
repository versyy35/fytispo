from django.urls import path
from . import views

urlpatterns = [

    path("", views.home, name = "home"),
    #path('home/', views.home, name='home'),  # Login/Registration Page URL
    path('login/', views.login_view, name='login'),  # Login Page URL
    path('logout/', views.logout_view, name='logout'),  # Logout Page URL
    path('register/', views.register, name='register'),  # Register Page URL
    path('userDashboard/', views.userDashboard_view, name='userDashboard'),  # User profile dashboard URL
    path('artistDashboard/', views.artistDashboard_views, name='artistDashboard'),
    path('modDashboard/', views.modDashboard_views, name = 'modDashboard'),
    path('musicPlayer/', views.musicPlayer_view, name='musicPlayer'),  # Music player URL
    path('imfeelinglucky/',views.imfeelinglucky_view, name ='imfeelinglucky'), # surprise URL
    path('listPlaylist/',views.listPlaylist_view, name ='listPlaylist'), # view playlists URL
    path('listArtist/', views.listArtist_view, name='listArtist'),
    path('artist/<str:artist_username>/songs/', views.artist_songs_view, name='artist_songs'),
    path('readAnnouncement/',views.readAnnouncement_view, name = 'readAnnouncement'), # read announcements URL
    path('viewPlaylist/<int:playlist_id>/', views.viewPlaylist_view, name='viewPlaylist'),
    path('modDashboard/modFlag/', views.modFlag_views, name='modFlag'),
    path('modDashboard/modFlag/delete/<int:flag_id>/', views.delete_flag_report, name='delete_flag_report'),
    path('modDashboard/postAnnouncement/', views.postAnnouncement_view, name='postAnnouncement'),
    path('delete_announcement/<int:announcement_id>/', views.delete_announcement, name='delete_announcement'),
    path("upload_song/", views.upload_song_view, name='upload_song'),
    path('add_to_playlist/<int:song_id>/', views.add_to_playlist, name='add_to_playlist'),
    path('create_playlist/', views.create_playlist, name='create_playlist'),
    path('delete_playlist/<int:playlist_id>/', views.delete_playlist, name='delete_playlist'),
    path('rename_playlist/<int:playlist_id>/', views.rename_playlist, name='rename_playlist'),
    path('share_playlist/<int:playlist_id>/', views.share_playlist, name='share_playlist'),
    path('flag_announcement/<int:announcement_id>/', views.flag_announcement, name='flag_announcement')
]