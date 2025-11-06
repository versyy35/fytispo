from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from django.utils import timezone

# Create your models here.

# ------------------- ROLE MODEL -------------------
class Role(models.Model): 
    role_id = models.AutoField(primary_key=True)  # Primary Key (Auto-incremented)
    role_name = models.CharField(max_length=50, unique=True)  

    def __str__(self): 
        return self.role_name

# ------------------- USER MODEL -------------------
class User(AbstractUser):  
    user_id = models.AutoField(primary_key=True)  # Primary Key (Auto-incremented)
    email = models.EmailField(unique=True, null=False)  
    created_at = models.DateTimeField(auto_now_add=True)  
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name="users")  # Foreign Key to Role

    groups = models.ManyToManyField(
        "auth.Group",
        related_name="custom_user_groups",  # Prevents conflict
        blank=True
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="custom_user_permissions",  # Prevents conflict
        blank=True
    )

    def __str__(self): 
        return self.username 

# ------------------- CONTENT MODEL -------------------
class Content(models.Model):  
    content_id = models.AutoField(primary_key=True)  # Primary Key (Auto-incremented)
    content_type = models.CharField(max_length=255)  

    def __str__(self): 
        return self.content_type

# ------------------- SONG MODEL -------------------
class Song(models.Model): 
    song_id = models.AutoField(primary_key=True)  # Auto-incremented primary key
    title = models.CharField(max_length=255)  
    genre = models.CharField(max_length=255)  
    duration = models.IntegerField()  # Store in seconds

    play_count = models.IntegerField(default=0)  # Default to 0
    audio_file = models.FileField(upload_to='media/songs/')  # Store audio files

    upload_date = models.DateTimeField(auto_now_add=True)  # Auto timestamp

    # Foreign Keys  
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="songs")  
    content = models.ForeignKey("Content", on_delete=models.CASCADE, related_name="songs")  
    flag_report = models.ForeignKey("FlagReport", on_delete=models.SET_NULL, null=True, blank=True, related_name="flagged_songs")  

    def __str__(self): 
        return f"{self.title} - {self.user.username}"

# ------------------- PLAYLIST MODEL -------------------
class Playlist(models.Model): 
    playlist_id = models.AutoField(primary_key=True)  # Primary Key (Auto-incremented)
    title = models.CharField(max_length=255)  

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="playlists")  # Foreign Key to User (Playlist Owner)
    content = models.ForeignKey(Content, on_delete=models.CASCADE, related_name="playlists")  # Foreign Key to Content
    flag_report = models.ForeignKey("FlagReport", on_delete=models.SET_NULL, null=True, blank=True, related_name="flagged_playlists")  # Foreign Key to FlagReport

    def __str__(self): 
        return self.title

# ------------------- PLAYLIST-SONG RELATION MODEL -------------------
class PlaylistSong(models.Model):  
    song = models.ForeignKey(Song, on_delete=models.CASCADE, related_name="playlist_songs")  # Foreign Key to Song
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE, related_name="playlist_songs")  # Foreign Key to Playlist
    added_at = models.DateTimeField(auto_now_add=True)  

    class Meta:
        unique_together = ('song', 'playlist')  # Ensures a song isn't added twice to the same playlist

    def __str__(self): 
        return f"Song '{self.song.title}' in Playlist '{self.playlist.title}'"

# ------------------- ANNOUNCEMENT MODEL -------------------
class Announcement(models.Model):
    announcement_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    content_text = models.TextField(max_length=500)
    posted_at = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="announcements")
    content = models.ForeignKey(Content, on_delete=models.CASCADE, related_name="announcements", null=True, blank=True)  # Add this line
    flag_report = models.ForeignKey("FlagReport", on_delete=models.SET_NULL, null=True, blank=True, related_name="flagged_announcements")
    def __str__(self):
        return self.title


# ------------------- FLAG REPORT MODEL -------------------
class FlagReport(models.Model):  
    flag_id = models.AutoField(primary_key=True)  # Primary Key (Auto-incremented)
    reason = models.CharField(max_length=255)  
    date_flagged = models.DateTimeField(auto_now_add=True)  

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="flag_reports")  # Foreign Key to User (Who flagged it)
    content = models.ForeignKey(Content, on_delete=models.CASCADE, related_name="flag_reports")  # Foreign Key to Content

    def __str__(self): 
        return f"Flagged by {self.user.username} - {self.reason}"

# ------------------- SHARED PLAYLIST MODEL -------------------
class SharedPlaylist(models.Model):
    shared_playlist_id = models.AutoField(primary_key=True)
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE, related_name="shared_playlists")
    shared_with = models.ForeignKey(User, on_delete=models.CASCADE, related_name="shared_playlists")
    shared_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('playlist', 'shared_with')  # Ensures a playlist isn't shared twice with the same user

    def __str__(self):
        return f"Playlist '{self.playlist.title}' shared with {self.shared_with.username}"