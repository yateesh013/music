import vlc  as v
import time as t

class music():
    #initializing the music playlist
    def __init__(self) -> None:
        #self.songs=[s[0][0],s[1][0],s[2][0]]
        self.songs=["E:\\MY FIlES  Y\\all songs\\Ala-Vaikuntapuramlo\\Butta Bomma-Naasongs.fm.mp3","C:\\Users\\DELL\\Desktop\\PAT_13_02_24\\joviandsa\\v.mp3","C:\\Users\\DELL\\Desktop\\PAT_13_02_24\\joviandsa\\a.mp4"]
        self.loop=[2,0,1]
        self.portions=[[(0.8,0.85)],[(0.5,0.52)],[(0.5,0.51)]]
        self.start()
    #start executing the playlist
    def start(self,ind=0):
        self.ind=ind
        self.play()
    #plays the track 
    def play(self):
        #checking if there are any loops 
        # or just to play the tracks inorder
        if len(self.loop)==0:
            k=self.ind
        else:
            k=self.loop[self.ind]    
        
        #taking th epath of track
        track=self.songs[k]  
        self.p=v.MediaPlayer(track)

        #checking there are any portions for the track     
        if len(self.portions[k])==0:
            self.p.play()
        else:
            #playing the portions if any 
            for i in self.portions[k]: 
                self.p.play()
                self.p.set_position(i[0])
                while self.p.get_position()<i[1]:
                    pass
                self.next()        

        t.sleep(2)
        while self.p.get_position()<0.98:
            pass
        self.next()
        ac=0
        #controls in console not used ,updated for gui
        while self.p.is_playing() and ac!="":
            if ac==" ":
                break
            elif ac=="p":
                self.pause()
            elif ac=="n":
                self.next()
            elif ac=="pr":
                self.prev() 
    
    #resume,play the track
    def pause(self):
        self.p.pause()

    #playing next track
    def next(self):
        self.p.stop()
        self.ind+=1
        if self.ind==len(self.songs):
            self.ind=0
        self.play() 
    #playing the previous track
    def prev(self):
        self.p.stop()
        self.ind-=1
        if self.ind==-1:
            self.ind=len(self.songs)-1
        self.play()     


#calling the music class
o=music()
o.start()


