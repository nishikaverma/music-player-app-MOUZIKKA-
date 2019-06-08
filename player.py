import model
from pygame import mixer
from tkinter import filedialog
import os
from mutagen.mp3 import MP3

class player:

    def __init__(self):
        mixer.init() # to load music player
        self.my_model=model.model()

    def get_db_status(self):
        return self.my_model.get_db_status()

    def close_player(self):
        mixer.music.stop() # to unload the music player
        self.my_model.close_db_connection()

    def set_volume(self,volume_level):
        mixer.music.set_volume(volume_level)

    def add_song(self):

        song_path = filedialog.askopenfilename(title="select any song",filetypes=[("mp3 files",".mp3")])
        if song_path == "":
            return
        else:
            song_name=os.path.basename(song_path) # takes complete path as a string  and returns  only the file name
            print("song path is :",song_path)
            print("song name is: ",song_name)
            self.my_model.add_song(song_name,song_path) # calling "add_song" method of module "model"
            return song_name

    def remove_song(self,song_name):
        self.my_model.remove_song(song_name) # calling "remove_song" method of  module "model"

    def get_song_length(self,song_name):
        self.song_path=self.my_model.get_song_path(song_name)  # calling "get_song_path" method of  module "model" for
        self.obj_mp3 = MP3(self.song_path) # creating object of class "MP3" whose constructor is parameterized
        return self.obj_mp3.info.length

    def play_song(self):
        mixer.quit()  # to un-initialize the mixer
        mixer.init(frequency=self.obj_mp3.info.sample_rate) # for getting the playback speed of MP3 file and  for again initializing mixter , it can also take playback speed [here- frequency_rate] as argument
        mixer.music.load(self.song_path) # for loading the song
        mixer.music.play() # for playing the song


    def stop_song(self):
        mixer.music.stop()

    def pause_song(self):
        mixer.music.pause()

    def unpause_song(self):
        mixer.music.unpause()

    def add_song_to_favourite(self,song_name):
        song_path = self.my_model.get_song_path(song_name) # to get the song path
        result=self.my_model.add_song_to_favourites(song_name,song_path)
        return result

    def load_songs_from_favourites(self):
        result= self.my_model.load_songs_from_favourites()
        return result,self.my_model.song_dict

    def remove_song_from_favourites(self,song_name):
        result = self.my_model.remove_song_from_favourites(song_name)
        return result




