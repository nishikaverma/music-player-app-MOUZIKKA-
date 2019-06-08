from cx_Oracle import *
from tkinter import messagebox
import player

class model:

    def __init__(self):
        self.song_dict={}
        self.db_status=True
        self.conn=None
        self.cur=None

        try:
            self.conn=connect("system/oracle123@localhost/orcl")
            print("connection established")
            self.cur=self.conn.cursor()
        except (DatabaseError) as e:
            print("Error :",e)
            self.db_status=False

    def get_db_status(self):
        return self.db_status

    def close_db_connection(self):
        if self.cur is not None:
            self.cur.close()
            print(" cursor connection closed !")

        if self.conn is not None:
            self.conn.close()
            print("database connection closed !")

    def add_song(self,song_name,song_path):
        self.song_dict[song_name] = song_path
        print("Song added , ",self.song_dict[song_name])

    def get_song_path(self,song_name):
        return self.song_dict[song_name]

    def remove_song(self,song_name):
        self.song_dict.pop(song_name)
        print("song removed ")
        print(self.song_dict)

    def search_song_in_favourites(self,song_name):


        '''  # my logic :

        self.cur.execute("select sname from MyFavourites ")

        if song_name in sname:
            print('song present in favourites')
            return True
        else:
            print("song not present")
            return False'''

        self.cur.execute("select sname from MyFavourites where sname= :1",(song_name,))
        song_tuple= self.cur.fetchone()
        if song_tuple is None:
            return False
        else:
            return True



    def add_song_to_favourites(self,song_name,song_path):

        ''' # my logic :
        is_song_present = self.search_song_in_favourites(song_name)
        if is_song_present==True:
            messagebox.showinfo("INFORMATION ","Song already present in Favourites ;-) ")
        else:
            self.cur.execute("Select sname,sid from MyFavourites")
            song_list= self.cur.fetchall()
            if len(song_list) == 0: # if there is no song present in favourite list
                new_song_id = 1
            else:
                song_tuple =song_list[-1]
                n=int(song_tuple[1])
                new_song_id = n+1
            self.cur.execute("Insert into MyFavourites(sname,spath,sid)  values(song_name,song_path,new_song_id)")
            self.conn.commit()
            print("song added to favourite !")
            messagebox.showinfo(" info...", "Song added to favourites ;-) ") '''

        is_song_present = self.search_song_in_favourites(song_name)
        if is_song_present:
            return "Song already present in your favourites"
        self.cur.execute("select max(sid) from MyFavourites")
        last_song_id = self.cur.fetchone()[0]
        next_song_id = 1
        if last_song_id is not None:
            next_song_id = last_song_id + '1'

        self.cur.execute("insert into MyFavourites values(:1,:2,:3)", (song_name, song_path, next_song_id))
        self.conn.commit()
        return "Song added to your favourites"

    def load_songs_from_favourites(self):
        self.cur.execute("select sname,spath from MyFavourites")
        songs_present=False
        if self.cur is not None:
            for song_name,song_path in self.cur:
                self.song_dict[song_name]=song_path
                songs_present=True
        if songs_present == True:
            return "List populated from favourites"
        else:
            return "No song present in your favourites"

    def remove_song_from_favourites(self,song_name):
        self.cur.execute("delete from MyFavourites where sname=:1",(song_name,))
        n=self.cur.rowcount
        if n==0:
            return "Song not present in your favourites"
        else:
            self.remove_song(song_name)
            self.conn.commit()
            return "song deleted from favourites !"



'''if __name__=="__main__":
    p = player.player()
    print("DB status: ",p.get_db_status())
    p.add_song() '''


