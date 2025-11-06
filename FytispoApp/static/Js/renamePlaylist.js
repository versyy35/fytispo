// listPlaylist.html
function renamePlaylist(playlistId) {
    const newTitle = prompt("Enter the new title for the playlist:");
    if (newTitle) {
        fetch(`/rename_playlist/${playlistId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': '{{ csrf_token }}',
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ title: newTitle }),  // Send the new title in the request body
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert("Playlist renamed successfully!");
                window.location.reload(); // Refresh the page
            } else {
                alert("Failed to rename playlist: " + data.message);
            }
        })
        .catch(error => {
            console.error("Error:", error);
            alert("An error occurred while renaming the playlist.");
        });
    }
}