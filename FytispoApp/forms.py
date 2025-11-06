from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    account_type = forms.ChoiceField(
        choices=[("Listener", "Listener"), ("Music Artist", "Music Artist")],
        widget=forms.RadioSelect,
        required=True
    )

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2", "account_type"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove the default help_text
        for field in self.fields:
            self.fields[field].help_text = None

class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ['title', 'content_text']

class AddToPlaylistForm(forms.Form):
    playlist = forms.ModelChoiceField(
        queryset=None,
        empty_label="Select a playlist",
        widget=forms.Select(attrs={'class': 'playlist-select'})
    )

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set the queryset to only show playlists owned by the current user
        self.fields['playlist'].queryset = Playlist.objects.filter(user=user)

class FlagAnnouncementForm(forms.Form):
    reason = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=True)

    class Meta:
        model = FlagReport
        fields = ['reason']