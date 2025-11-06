// Function to delete a playlist
function deletePlaylist(playlistId) {
    if (confirm("Are you sure you want to delete this playlist?")) {
        fetch(`/delete_playlist/${playlistId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': '{{ csrf_token }}',
                'Content-Type': 'application/json',
            },
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert("Playlist deleted successfully!");
                window.location.reload(); // Refresh the page
            } else {
                alert("Failed to delete playlist: " + data.message);
            }
        })
        .catch(error => {
            console.error("Error:", error);
            alert("An error occurred while deleting the playlist.");
        });
    }
}