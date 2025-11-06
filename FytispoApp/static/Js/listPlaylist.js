document.addEventListener("DOMContentLoaded", function () {
    const menuIcons = document.querySelectorAll(".menu-icon");

    menuIcons.forEach(icon => {
        icon.addEventListener("click", function (event) {
            const menu = this.nextElementSibling;
            menu.style.display = menu.style.display === "block" ? "none" : "block";

            event.stopPropagation();
        });
    });

    document.addEventListener("click", function () {
        document.querySelectorAll(".menu-options").forEach(menu => {
            menu.style.display = "none";
        });
    });
});

// Dummy functions for menu actions
function copyLink() {
    alert("Playlist link copied!");
}

function deletePlaylist() {
    alert("Playlist deleted!");
}

function renamePlaylist() {
    const newName = prompt("Enter new playlist name:");
    if (newName) {
        alert(`Renamed to "${newName}" (Not yet implemented)`);
    }
}
