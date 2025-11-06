from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Role)
admin.site.register(User)
admin.site.register(Content)
admin.site.register(Song)
admin.site.register(Playlist)
admin.site.register(PlaylistSong)
admin.site.register(Announcement)
admin.site.register(FlagReport)

