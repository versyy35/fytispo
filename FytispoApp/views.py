from urllib import request
from django.shortcuts import *
from FytispoApp.forms import *
from django.contrib.auth import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Song
from django.shortcuts import render
from django.core.files.storage import default_storage
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json


def home(request):
    return render(request, 'home.html')


def register_view(request):
    return render(request, 'register.html')

def logout_view(request):
    logout(request)
    return redirect('home')

def login_view(request):
    error_message = None  # Initialize error_message to None by default

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        print(f"Login attempt - Username: {username}")  # Debug print

        # Check if user exists first
        from django.contrib.auth import get_user_model
        User = get_user_model()
        user_exists = User.objects.filter(username=username).exists()
        print(f"User exists in database: {user_exists}")  # Debug print
        
        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        print(f"Authentication result: {user is not None}")  # Debug print

        if user is not None:
            # Check if user has required attributes
            print(f"User role: {getattr(user, 'role', None)}")  # Debug print

            ## Check the user's role and redirect accordingly
            if user.role.role_name == "Listener":
                print("Redirecting to userDashboard")  # Debug print
                login(request, user)
                return redirect('userDashboard')  # Redirect to listener dashboard
            elif user.role.role_name == "Music Artist":
                print("Redirecting to artistDashboard")  # Debug print
                login(request, user)
                return redirect('artistDashboard')  # Redirect to artist dashboard
            elif user.role.role_name == "Moderator":
                print("Redirecting to modDashboard")  # Debug print
                login(request, user)
                return redirect('modDashboard')  # Redirect to moderator dashboard
            else:
                # Handle unknown roles (optional)
                error_message = "Your role is not recognized."
        else:
            # Display an error message
            error_message = "Invalid username or password."
            print("Authentication failed")  # Debug print
    
    return render(request, 'login.html', {'error_message': error_message})

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            # Create user but don't save to DB yet
            user = form.save(commit=False)
            
            # Get the role based on account_type
            role_name = form.cleaned_data["account_type"]
            try:
                role = Role.objects.get(role_name=role_name)
                user.role = role
                
                # Now save the user
                user.save()
                
                # Log the user in
                login(request, user)
                
                # Redirect to dashboard
                return redirect('userDashboard')
            
            except Role.DoesNotExist:
                form.add_error('account_type', 'Invalid role selected')
                return render(request, "register.html", {"form": form})
                
    else:
        form = RegisterForm()
    
    return render(request, "register.html", {"form": form})

def userDashboard_view(request):
    return render(request, 'userDashboard.html')

def musicPlayer_view(request):
    songs = Song.objects.all()  # Fetch all songs
    playlists = Playlist.objects.filter(user=request.user)  # Fetch playlists for the logged-in user
    return render(request, 'musicPlayer.html', {'songs': songs, 'playlists': playlists})



def imfeelinglucky_view(request):
    return render(request, 'imfeelinglucky.html')

@login_required
def listPlaylist_view(request):
    # Fetch playlists created by the user
    user_playlists = Playlist.objects.filter(user=request.user)
    
    # Fetch playlists shared with the user
    shared_playlists = Playlist.objects.filter(shared_playlists__shared_with=request.user)
    
    # Combine both lists
    playlists = user_playlists | shared_playlists
    
    return render(request, 'listPlaylist.html', {'playlists': playlists})

def listAlbum_view(request):
    return render(request, 'listAlbum.html')

def listArtist_view(request):
    # Get all users with the "Music Artist" role
    artists = User.objects.filter(role__role_name="Music Artist")
    return render(request, 'listArtist.html', {'artists': artists})

def artist_songs_view(request, artist_username):
    # Get the artist
    artist = get_object_or_404(User, username=artist_username, role__role_name="Music Artist")
    # Get all songs by this artist
    songs = Song.objects.filter(user=artist)
    return render(request, 'artist_songs.html', {'songs': songs, 'artist': artist})

def readAnnouncement_view(request):
    announcements = Announcement.objects.all().order_by('-posted_at')  # Fetch all announcements sorted by date
    return render(request, 'readAnnouncement.html', {'announcements': announcements})

def postAnnouncement_view(request):
    if request.method == 'POST':
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            announcement = form.save(commit=False)
            announcement.user = request.user  # Set the current user as the poster
            announcement.save()
            return redirect('readAnnouncement')  # Redirect to the announcements page
    else:
        form = AnnouncementForm()
    
    return render(request, 'postAnnouncement.html', {'form': form})

def viewPlaylist_view(request, playlist_id):
    # Check if the playlist belongs to the user or is shared with the user
    try:
        playlist = Playlist.objects.get(playlist_id=playlist_id, user=request.user)
    except Playlist.DoesNotExist:
        # If the playlist doesn't belong to the user, check if it's shared with the user
        try:
            playlist = Playlist.objects.get(playlist_id=playlist_id, shared_playlists__shared_with=request.user)
        except Playlist.DoesNotExist:
            # If the playlist doesn't exist or isn't shared with the user, raise a 404 error
            return get_object_or_404(Playlist, playlist_id=playlist_id)

    return render(request, 'viewPlaylist.html', {'playlist': playlist})


@login_required
def songList_eve_view(request):
    # Display all songs by Eve
    eve_user = User.objects.get(username='Eve')
    songs = Song.objects.filter(user=eve_user)
    return render(request, 'songList_eve.html', {'songs': songs})

@login_required
def songList_haruy_view(request):
    # Display all songs by Haruy
    haruy_user = User.objects.get(username='Haruy')
    songs = Song.objects.filter(user=haruy_user)
    return render(request, 'songList_haruy.html', {'songs': songs})

@login_required
def songList_higedan_view(request):
    # Display all songs by Higedan
    higedan_user = User.objects.get(username='Higedan')
    songs = Song.objects.filter(user=higedan_user)
    return render(request, 'songList_higedan.html', {'songs': songs})

def modDashboard_views(request):
    return render(request,'modDashboard.html')

@login_required
def modFlag_views(request):
    flagged_reports = FlagReport.objects.all().order_by("-date_flagged")  # Get all flag reports
    return render(request, 'modFlag.html', {"flagged_reports": flagged_reports})

@login_required
def mod_dashboard(request):
    flagged_songs = Song.objects.filter(flag_report__isnull=False)  # Get all flagged songs
    return render(request, "modDashboard.html", {"flagged_songs": flagged_songs})

@login_required
def modFlag_views(request):
    flagged_reports = FlagReport.objects.all().order_by("-date_flagged")  # Get all flag reports
    return render(request, 'modFlag.html', {"flagged_reports": flagged_reports})

@login_required
def delete_flag_report(request, flag_id):
    flag = get_object_or_404(FlagReport, flag_id=flag_id)
    flag.delete()
    messages.success(request, "Flag report deleted successfully!")
    return redirect("modFlag")


@login_required
def update_flag_status(request, song_id):
    song = get_object_or_404(Song, pk=song_id)

    if request.method == "POST":
        action = request.POST.get("action")
        moderator_comment = request.POST.get("moderator_comment", "").strip()

        if action == "unflag":
            # Remove the flag report from the song
            song.flag_report.delete()
            messages.success(request, "Song has been unflagged successfully.")
        elif action == "keep_flagged":
            # Keep the song flagged and optionally store moderator comments
            if moderator_comment:
                song.flag_report.moderator_comment = moderator_comment
                song.flag_report.save()
            messages.info(request, "Song remains flagged.")

        return redirect("moderator_dashboard")

    return render(request, "moderator_dashboard.html", {"flagged_songs": Song.objects.filter(flag_report__isnull=False)})


@login_required
def userDashboard(request):
    user = request.user
    
    # Add detailed debug prints
    print("DEBUG INFORMATION:")
    print(f"Is user authenticated: {request.user.is_authenticated}")
    print(f"User object: {user}")
    print(f"Username: {user.username}")
    print(f"Date joined: {user.date_joined}")
    
    context = {
        'username': user.username,
        'date_joined': user.date_joined.strftime('%d %B %Y'),
    }
    
    # Print the final context
    print(f"Context being sent to template: {context}")
    
    return render(request, 'userDashboard.html', context)

    
@login_required
def artistDashboard_views(request):
    request.user = get_user(request)  
    # Debugging: Print the logged-in user
    print(f"Logged-in user in artistDashboard: {request.user.username}")
    return render(request, 'artistDashboard.html')

@login_required
def upload_song_view(request):
    if request.method == 'POST':
        print("POST request received")  # Debugging
        print("POST data:", request.POST)  # Debugging
        print("FILES data:", request.FILES)  # Debugging
        print(f"Logged-in user before upload: {request.user.username}")  # Debugging

        title = request.POST.get('title')
        genre = request.POST.get('genre')
        duration = request.POST.get('duration')
        audio_file = request.FILES.get('audio_file')

        try:
            # Ensure the content type exists
            content, created = Content.objects.get_or_create(content_type='Song')

            # Save the file to the media directory
            file_path = default_storage.save('songs/' + audio_file.name, audio_file)

            # Create the song in the database
            Song.objects.create(
                title=title,
                genre=genre,
                duration=duration,
                audio_file=file_path,
                user=request.user,  # Assign the logged-in user
                content=content,
                play_count=0,
                flag_report=None
            )
            print("Song created successfully!")  # Debugging
            messages.success(request, "Song uploaded successfully!")
            return redirect('upload_song')  # Redirect back to the upload page

        except Exception as e:
            print("Error occurred:", e)  # Debugging
            messages.error(request, f"An error occurred: {e}")

    return render(request, 'upload_song.html')


def delete_announcement(request, announcement_id):
    if request.method == 'POST':
        # Ensure the user is a moderator
        if request.user.role.role_name != 'Moderator':
            messages.error(request, "You do not have permission to delete announcements.")
            return redirect('readAnnouncement')

        # Fetch the announcement
        announcement = get_object_or_404(Announcement, announcement_id=announcement_id)
        announcement.delete()
        messages.success(request, "Announcement deleted successfully.")
    
    return redirect('readAnnouncement')

def add_to_playlist(request, song_id):
    if request.method == 'POST':
        try:
            # Fetch the song and playlist
            song = Song.objects.get(song_id=song_id)
            playlist_id = request.POST.get('playlist_id')
            playlist = Playlist.objects.get(playlist_id=playlist_id, user=request.user)  # Ensure the playlist belongs to the user

            # Check if the song is already in the playlist
            if PlaylistSong.objects.filter(song=song, playlist=playlist).exists():
                messages.warning(request, "Song is already in the playlist.")
            else:
                # Add the song to the playlist
                PlaylistSong.objects.create(song=song, playlist=playlist)
                messages.success(request, "Song added to playlist successfully!")
        except Song.DoesNotExist:
            messages.error(request, "Song not found.")
        except Playlist.DoesNotExist:
            messages.error(request, "Playlist not found.")
        except Exception as e:
            messages.error(request, f"An error occurred: {e}")
    
    return redirect('musicPlayer')  # Redirect back to the music player page
@login_required
def create_playlist(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        if title:
            try:
                # Ensure the content type exists
                content, created = Content.objects.get_or_create(content_type='Playlist')

                # Create the playlist
                Playlist.objects.create(
                    title=title,
                    user=request.user,  # Assign the logged-in user
                    content=content,
                )
                messages.success(request, "Playlist created successfully!")
            except Exception as e:
                messages.error(request, f"An error occurred: {e}")
        else:
            messages.error(request, "Playlist title cannot be empty.")
    
    return redirect('listPlaylist')

@csrf_exempt
def delete_playlist(request, playlist_id):
    if request.method == 'POST':
        try:
            # Fetch the playlist
            playlist = Playlist.objects.get(playlist_id=playlist_id, user=request.user)  # Ensure the playlist belongs to the user
            playlist.delete()
            return JsonResponse({"success": True, "message": "Playlist deleted successfully!"})
        except Playlist.DoesNotExist:
            return JsonResponse({"success": False, "message": "Playlist not found."})
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)})
    else:
        return JsonResponse({"success": False, "message": "Invalid request method."})

@csrf_exempt
def rename_playlist(request, playlist_id):
    if request.method == 'POST':
        try:
            # Fetch the playlist
            playlist = Playlist.objects.get(playlist_id=playlist_id, user=request.user)  # Ensure the playlist belongs to the user

            # Parse the request body
            data = json.loads(request.body)
            new_title = data.get('title')
            if new_title:
                playlist.title = new_title
                playlist.save()
                return JsonResponse({"success": True, "message": "Playlist renamed successfully!"})
            else:
                return JsonResponse({"success": False, "message": "New title cannot be empty."})
        except Playlist.DoesNotExist:
            return JsonResponse({"success": False, "message": "Playlist not found."})
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)})
    else:
        return JsonResponse({"success": False, "message": "Invalid request method."})

@login_required
def share_playlist(request, playlist_id):
    if request.method == 'POST':
        username = request.POST.get('username')
        try:
            # Fetch the playlist and the user to share with
            playlist = get_object_or_404(Playlist, playlist_id=playlist_id, user=request.user)
            shared_with_user = get_object_or_404(User, username=username)

            # Check if the playlist is already shared with this user
            if SharedPlaylist.objects.filter(playlist=playlist, shared_with=shared_with_user).exists():
                messages.warning(request, f"Playlist already shared with {username}.")
            else:
                # Share the playlist
                SharedPlaylist.objects.create(playlist=playlist, shared_with=shared_with_user)
                messages.success(request, f"Playlist shared with {username} successfully!")
        except User.DoesNotExist:
            messages.error(request, f"User {username} not found.")
        except Exception as e:
            messages.error(request, f"An error occurred: {e}")

    return redirect('listPlaylist')

@login_required
def flag_announcement(request, announcement_id):
    if request.method == 'POST':
        reason = request.POST.get('reason')
        announcement = get_object_or_404(Announcement, announcement_id=announcement_id)
        
        # Ensure the content type exists
        content, created = Content.objects.get_or_create(content_type='Announcement')
        
        # Create the flag report
        flag_report = FlagReport.objects.create(
            reason=reason,
            user=request.user,
            content=content,
        )
        
        # Link the flag report to the announcement
        announcement.flag_report = flag_report
        announcement.save()
        
        messages.success(request, "Announcement flagged successfully.")
    
    return redirect('readAnnouncement')