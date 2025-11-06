// JavaScript for Music Player
const audioPlayer = document.getElementById('audioPlayer');
const songTitle = document.getElementById('songTitle');
const songArtist = document.getElementById('songArtist');
const volumeControl = document.getElementById('volumeControl');

// Function to play a song
function playSong(url, title, artist) {
    audioPlayer.src = url;
    audioPlayer.play();
    songTitle.textContent = title;
    songArtist.textContent = artist;
}

// Adjust volume
volumeControl.addEventListener('input', () => {
    audioPlayer.volume = volumeControl.value;
});