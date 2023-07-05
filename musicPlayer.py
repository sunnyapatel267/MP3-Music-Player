import pygame
from tkinter import *
from tkinter import filedialog
from tkinter import simpledialog
from PIL import ImageTk,Image
import json
import os
import eyed3
import file1

root = Tk()
root.title('Music Player')
root.geometry("900x700")
root.resizable(False,False)
root.configure(bg="#ffffff")
pygame.init()

class playlist:
    global add_oneSong, add_multipleSong, create_Playlist, closePOPUP,load_playlist, open_Playlist, save_Playlist
    def add_oneSong():
        song = filedialog.askopenfilename(title="Choose a Song", filetypes=(("mp3 Files", "*.mp3"),))
        song = song.replace(file1.file_address, "")
        song = song.replace(".mp3", "")
        playlistOfSongs.insert(END,song)

    def add_multipleSong():
        songs = filedialog.askopenfilenames(title="Choose Songs",filetypes=(("mp3 Files", "*.mp3"),))
        songList = list(songs)
        for song in songList:
            song = song.replace(file1.file_address, "")
            song = song.replace(".mp3", "")
            playlistOfSongs.insert(END,song)

    def create_Playlist():
        userInput_Playlist_Name = simpledialog.askstring(title=" ",prompt="Enter Playlist Name:")
        userInput_Playlist_Name = userInput_Playlist_Name + ".json"
        songs = filedialog.askopenfilenames(title="Choose Songs",filetypes=(("mp3 Files", "*.mp3"),))
        playlist = list(songs)
        with open("playlists/"+userInput_Playlist_Name,"w") as file:
            json.dump(playlist, file)

    def closePOPUP():
        global playlist_location
        playlist_location = " "
        if file_listbox.curselection():
            playlist_location = file_listbox.get(file_listbox.curselection())
        playlist_location = os.path.join(folder_path,playlist_location+".json")
    
        load_playlist()
        popup.destroy()

    def load_playlist():
        global playlist_location
        try:
            with open(playlist_location, "r") as file:
                playlist = json.load(file)
                playlistOfSongs.delete(0,END)

                for song in playlist:
                    song = song.replace(file1.file_address, "")
                    song = song.replace(".mp3", "")
                    playlistOfSongs.insert(END, song)

                labelPlaylist = playlist_location
                labelPlaylist = labelPlaylist.replace("playlists/","")
                labelPlaylist = labelPlaylist.replace(".json","")
                playlist_name_label.config(text=f"Playlist: {labelPlaylist}")

        except FileNotFoundError:
            print("Playlist not found: " + playlist_location)

    def open_Playlist():
        global playlist_location
        global folder_path
        folder_path = "playlists"
        files = os.listdir(folder_path)

        global popup
        popup = Toplevel(root)
        popup.geometry("200x250")
        global file_listbox
        file_listbox = Listbox(popup)
        file_listbox.pack()

        for file in files:
            file = file.replace(".json","")
            file_listbox.insert(END, file)

        open_button = Button(popup, text="Open", command = closePOPUP)
        open_button.pack()
    
    def save_Playlist():
        data = []
        with open(playlist_location , "w") as file:
            json.dump(data, file, indent = 4)

        listOfSongs = list(playlistOfSongs.get(0,END))
        with open(playlist_location, "w") as file:
            json.dump(listOfSongs, file, indent = 4)


playlistOfSongs = Listbox(root,bg="#fc3535",fg="white", bd = 0 , width = 20, height = 20, font=("MS Sans Serif",20), justify=CENTER, selectbackground="#f76363")
playlistOfSongs.place(x = 620, y = 80)

my_menu = Menu(root)
root.config(menu=my_menu)
add_song_menu = Menu(my_menu)

my_menu.add_cascade(label="Add Songs", menu= add_song_menu)
add_song_menu.add_command(label= "Add One Song to Playlist", command= add_oneSong)
add_song_menu.add_command(label="Add Multiple Songs to Playlist", command=add_multipleSong)

create_playlist_menu = Menu(my_menu)
my_menu.add_cascade(label="Playlist", menu= create_playlist_menu)
create_playlist_menu.add_command(label="Create a Playlist", command=create_Playlist)
create_playlist_menu.add_command(label="Open Playlist", command=open_Playlist)
create_playlist_menu.add_command(label="Save", command=save_Playlist)

global playlist_name_label
playlist_name_label = Label(root, text= "Playlist: None", bg="#ffffff",fg = "black", font=("MS Sans Serif",15) )
playlist_name_label.pack()
playlist_name_label.place(x=700,y=47)

global current_song_playing_label
current_song_playing_label = Label(root, text = " ",  bg="#ffffff",fg = "black", font=("MS Sans Serif",30))
current_song_playing_label.pack()
current_song_playing_label.place(relx=0.34, x = 0, y = 500, anchor="center")

global current_image
current_image = None
global music_art
music_art = Label(root) 

class buttons:
    #This class has buttons such as:pause, play, unpause, and etc.
    global hideButton, showButton, playAudio, startAudio, pauseAudio, unpause, next_Song, back_Song, extractImage, display_image

    def display_image(image_path):
        if image_path is not None:
            global current_image
            image1 = Image.open(image_path)
            image1.thumbnail((400,400))
            current_image = ImageTk.PhotoImage(image1)
            music_art.config(image=current_image)
            music_art.pack()
            music_art.place(x=100,y=50)

    def extractImage(mp3FilePath, outputImagePath):
        audio = eyed3.load(mp3FilePath)
        if audio.tag and audio.tag.images:
            image_data = audio.tag.images[0].image_data
            with open(outputImagePath, 'wb') as image_file:
                image_file.write(image_data)

    def hideButton(widget):
        widget.place_forget()

    def showButton(widget,xPos,yPos):
        widget.pack()
        widget.place(x = xPos, y = yPos)

    def playAudio():
        songLocation = playlistOfSongs.get(playlistOfSongs.curselection())
        current_song_playing_label.config(text = f"{songLocation}")
        songLocation = file1.file_address + songLocation + ".mp3"
        musicImage = " "
        extractImage(songLocation,musicImage)
        print(musicImage)
        display_image(musicImage)
        pygame.mixer.music.load(songLocation)
        pygame.mixer.music.play()

    def startAudio():
        playAudio()
        hideButton(playButton)
        showButton(pauseButton, 400, 550)
        hideButton(unpauseButton)
    
    def pauseAudio():
        pygame.mixer.music.pause()
        hideButton(pauseButton)
        showButton(playButton, 400, 550)

    def unpause():
        pygame.mixer.music.unpause()
        hideButton(unpauseButton)
        showButton(pauseButton, 400, 550)

    def next_Song():
        nextSongLocation = playlistOfSongs.curselection()
        if playlistOfSongs.size() == (nextSongLocation[0]+1):
            nextSongLocation = 0
        else:
            nextSongLocation = nextSongLocation[0]+1

        songName = playlistOfSongs.get(nextSongLocation)
        current_song_playing_label.config(text = f"{songName}")
        
        songName = file1.file_address + songName + ".mp3"
        musicImage = " "
        extractImage(songName,musicImage)
        display_image(musicImage)

        pygame.mixer.music.load(songName)
        pygame.mixer.music.play()

        playlistOfSongs.selection_clear(0,END)
        playlistOfSongs.activate(nextSongLocation)
        playlistOfSongs.selection_set(nextSongLocation, last= None)
        
        hideButton(playButton)
        hideButton(unpauseButton)
        showButton(pauseButton, 400, 550)

    def back_Song():
        backSongLocation = playlistOfSongs.curselection()
        if int(backSongLocation[0]) == int(0):
            backSongLocation = playlistOfSongs.size() - 1
        else:
            backSongLocation = backSongLocation[0] - 1

        songName = playlistOfSongs.get(backSongLocation)
        current_song_playing_label.config(text = f"{songName}")
        
        songName = file1.file_address + songName + ".mp3"
        musicImage = " "
        extractImage(songName,musicImage)
        display_image(musicImage)

        pygame.mixer.music.load(songName)
        pygame.mixer.music.play()

        playlistOfSongs.selection_clear(0,END)
        playlistOfSongs.activate(backSongLocation)
        playlistOfSongs.selection_set(backSongLocation, last= None)

        hideButton(playButton)
        hideButton(unpauseButton)
        showButton(pauseButton, 400, 550)

    #End of Button Class

global unpauseButton
global playButton
global pauseButton

img1 = Image.open("buttonImage/newPause.jpg")
img1 = img1.resize((40,40), resample=Image.LANCZOS)
pauseImage = ImageTk.PhotoImage(img1)
img2 = Image.open("buttonImage/newPlay.jpg")
img2 = img2.resize((40,40), resample=Image.LANCZOS)
playImage = ImageTk.PhotoImage(img2)
img3 = Image.open("buttonImage/newBack.jpg")
img3 = img3.resize((40,40), resample=Image.LANCZOS)
backImage = ImageTk.PhotoImage(img3)
img4 = Image.open("buttonImage/newNext.jpg")
img4 = img4.resize((40,40), resample=Image.LANCZOS)
nextImage = ImageTk.PhotoImage(img4)

unpauseButton = Button(root, text = "Play", command = unpause,image=pauseImage, highlightthickness= 0, padx=0, pady=0, bd = 0)
hideButton(unpauseButton)
playButton = Button(root, text = "Play", command = startAudio,image=playImage, highlightthickness= 0, padx=0, pady=0, bd = 0)
pauseButton = Button(root, text = "Pause", command = pauseAudio,image=pauseImage, highlightthickness= 0, padx=0, pady=0, bd = 0)
hideButton(pauseButton)
nextButton = Button(root, text = "", command = next_Song,image=nextImage, highlightthickness= 0, padx=0, pady=0, bd = 0)
backButton = Button(root, text = "Back", command = back_Song,image=backImage, highlightthickness= 0, padx=0, pady=0, bd = 0)
createPlaylist = Button(root, text = "Create Playlist", command=create_Playlist, highlightbackground = "#ffffff")
openPlaylist = Button(root, text = "Open Saved Playlist", command=open_Playlist, highlightbackground = "#ffffff")

backButton.pack()
backButton.place(x = 300, y = 550)
playButton.pack()
playButton.place(x = 400, y = 550)
nextButton.pack()
nextButton.place(x = 500, y = 550)
createPlaylist.pack()
createPlaylist.place(x = 750, y = 10)
openPlaylist.pack()
openPlaylist.place(x = 600, y = 10)

root.mainloop()