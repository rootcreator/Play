$(document).ready(function() {
    // Hide all sections except the Albums section on page load
    $("section:not(#albums)").hide();

    // Handle navigation clicks
    $("ul.navbar-nav a").click(function(event) {
        event.preventDefault();
        var targetSection = $(this).attr("href");
        $("section").hide();
        $(targetSection).show();
    });

    // View Songs button click handler
    $(".view-songs").click(function() {
        var albumId = $(this).closest("[data-album-id]").data("album-id");
        $("#albumSongsList li").hide();
        $("#albumSongsList li[data-album-id='" + albumId + "']").show();
        $("#songs").show();
    });

    // Play audio
    function playAudio(audioUrl) {
        var audioPlayer = $("#audioPlayer");
        audioPlayer.attr("src", audioUrl);
        audioPlayer.trigger("play");
    }

    // Play button click handler for individual songs
    $("section#songs button").click(function() {
        var audioUrl = $(this).closest("li").find("button").data("audio-url");
        playAudio(audioUrl);
        var songInfo = $(this).closest("li").text();
        $("#currentSongInfo").text("Now playing: " + songInfo);
    });

    // Handle click on artist or genre items
    $(".artist-item, .genre-item").click(function() {
        var filterValue = $(this).data("artist") || $(this).data("genre");
        $("#albumList > div").hide();
        $("#albumList > div:has(p:contains('" + filterValue + "'))").show();
        $("#albums").show();
    });
});
