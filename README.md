# MP3-Music-Player

This is a MP3 music player application devolped Python and various libraries. It allows the user to create playlists, add songs to playlists, and play song from the playlist. This application has graphical user interface built using the Tkinter library.

## Features
- Add one song to the playlist
- Add multiple songs to the playlist
- Create a new playlist
- Open an existing playlist
- Save current playlist
- Play, pause, and control the playback of songs
- Display the currently playing song and its associated albumn artwork

## Prerequisites
Before running the application, make sure you have the following libraries installed: 
- `pygame`
- `tkinter`
- `PIL`
- `json`
- `os`
- `eyed3`

## Getting Started
1. Clone the repository or copy the code into your local environment.
2. Make sure all the required libraries are installed.

## How to Use

- Add Songs:
  - Choose one song: Select a single MP3 file and add it to the playlist.
  - Choose multiple songs: Select multiple MP3 files and add them to the playlist.

- Playlist:
  - Create a Playlist: Create a new playlist by providing a name and selecting songs to add to it.
  - Open Playlist: Open an existing playlist from the saved playlists.
  - Save: Save the current playlist.

- Playback Controls:
  - Play: Start playing the selected song.
  - Pause: Pause the currently playing song.
  - Unpause: Resume playing the paused song.
  - Next: Play the next song in the playlist.
  - Back: Play the previous song in the playlist.

- Playlist Display:
  - The playlist is displayed on the right side of the window.
  - The currently playing song is displayed in the "Current Song" label.
  - The album artwork associated with the currently playing song is displayed.
