import customtkinter as ct
from tkinter import ttk
from tkinter import filedialog
import db_func as db
import vlc as v


class app(ct.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("700x500")
        self.title("MY MUSIC")
        ct.set_appearance_mode("dark")
        ct.set_default_color_theme("blue")
        self.resizable("False","False")
        

    def main_window(self):
    
        l1=ct.CTkLabel(self,text=" MY MUSIC ",text_color="black",bg_color="Green")
        l1.place(x=20,y=20)
        t1=ct.CTkLabel(self,text="YOUR PLAYLISTS:",font=("helvitica",13),text_color="black")
        t1.place(x=100,y=40)

        playarea=ct.CTkScrollableFrame(self,orientation="vertical",height=70,width=300,scrollbar_button_hover_color="green")
        playarea.place(x=50,y=70)
        col=["name","count"]
        self.tree1=ttk.Treeview(playarea,columns=col,show="headings")
        self.tree1.pack()
        self.tree1.heading("name",text="PLAYLIST")
        self.tree1.column(column="name",width=250)
        self.tree1.heading("count",text="NO")
        self.tree1.column(column="count",width=50)
        self.playlists=db.read_data()
        #self.playlists=[("1","2","1","1"),("2","5","1","1"),("3","6","1","1")]
    
        def addplaylist():
            new=ct.CTkToplevel()
            new.geometry("300x300")
            new.resizable(False,False)
            l1=ct.CTkLabel(new,text="NAME :")
            l1.place(x=50,y=50)
            e1=ct.CTkEntry(new,placeholder_text="enter name",placeholder_text_color="green",corner_radius=25)
            e1.place(x=100,y=50)
            
            def add():
                name=e1.get()
                new.destroy()
                self.playlists.append((name,0))
                self.display(songs=False)

            b1=ct.CTkButton(new,text="ADD",fg_color="green",text_color="black",hover_color="green",corner_radius=25,command=add)
            b1.place(x=150,y=150)
        self.display(songs=False)
        self.tree1.bind("<<TreeviewSelect>>",self.open_play)
        add_b=ct.CTkButton(self,text="+",command=addplaylist,
                           font=("helvitica",25),corner_radius=25,width=100,hover_color="green")
        add_b.place(x=100,y=300)
    


    def open_play(self,s):
        num=self.tree1.focus()
        num1=self.tree1.item(num)
        data=num1["values"]
        try:
            self.playlist=data[0]
        except:
            self.playlist=" "
        
        def delete_playlist():
            ind=None
            temp=num1["values"][0]
            for i in range(len(self.playlists)):
                if self.playlists[i][0]==temp:
                    ind=i
            if ind is not None:        
                self.playlists.pop(ind)
                self.display(songs=False)
                data[0]=""
                self.clear()   
        del_b=ct.CTkButton(self,command=delete_playlist,text="--",font=("helvitica",25),corner_radius=25,width=100,hover_color="green")
        del_b.place(x=260,y=300)
        tree_2=ct.CTkScrollableFrame(self,height=200,width=250,scrollbar_button_hover_color="green")
        tree_2.place(x=400,y=70)
        col=["name"]
        self.tree2=ttk.Treeview(tree_2,columns=col,show="headings")
        self.tree2.pack()
        self.tree2.heading("name",text="SONG")
        self.tree2.column(column="name")
        self.songs=db.read_data(name=self.playlist)
        print(self.songs)
        self.songs=[("4","2","1","1"),("5","5","1","1"),("6","6","1","1")]
        self.display()
        self.player(s)
        self.tree2.bind("<<TreeviewSelect>>",self.player)    
    
    def player(self,s):  
        #simple player  
        p_frame=ct.CTkFrame(self,width=150,height=50)
        p_frame.place(x=150,y=420)
        
        def test(s):
            pos=self.p.get()
            num=self.tree2.focus()
            num1=self.tree2.item(num)
            data=num1["values"]
            #print(data)
            #play(pos,data[1],data[2])
        
        self.p=ct.CTkSlider(p_frame,fg_color="black",progress_color="green",orientation="horizontal",
                       width=400,height=10,command=test)
        self.p.pack()


    
        p_b1=ct.CTkButton(self,text="|<",  
                        text_color="black",hover_color="green",width=75,corner_radius=25,
                        font=("helvetica",20))
        p_b1.place(x=220,y=450)
        p_b2=ct.CTkButton(self,text="||",
                        text_color="black",hover_color="green",width=75,corner_radius=25,
                        font=("helvetica",20))
        p_b2.place(x=310,y=450)
        p_b3=ct.CTkButton(self,text=">|",
                        text_color="black",hover_color="green",width=75,corner_radius=25,
                        font=("helvetica",20))
        p_b3.place(x=400,y=450)
        
        #playlist changes can be done here
        def addsong():
            file=filedialog.askopenfile("r")
            p=file.name
            for i in range(len(p)-1,-1,-1):
                 if p[i]=="/":
                      temp=p[i+1:]
                      break
            
            p=p.replace("/","//")
            instance=v.Instance()
            m=instance.media_new(p)
            l=int(m.get_duration()/1000)
            for i in range(len(self.playlists)):
                if self.playlists[i][0]==self.playlist:
                    t=self.playlists[i][1]
                    d=list(self.playlists[i])  
                    d[1]=t
                    self.playlists[i]=tuple(d)
                    print(self.playlists)
                    break                   
            self.songs.append((temp,p,l,"1"))
            print(self.songs)
            self.display() 
            self.display(songs=False)      
    
        def deletesong():
            num=self.tree2.focus()
            num1=self.tree2.item(num)
            data=num1["values"]
            print(self.songs,data[1])
            for i in range(len(self.songs)):
                if self.songs[i][1]==str(data[1]):
                    ind=i
                    break
            self.songs.pop(ind)                    
            self.display()
       
        pl_b1=ct.CTkButton(self,text="↑",
                        text_color="black",hover_color="green",width=50,corner_radius=25,
                        font=("helvetica",15))
        pl_b1.place(x=420,y=300)
        
        pl_b2=ct.CTkButton(self,text="↓",
                        text_color="black",hover_color="green",width=50,corner_radius=25,
                        font=("helvetica",15))
        pl_b2.place(x=490,y=300)
        
        pl_b3=ct.CTkButton(self,text="+",command=addsong,
                        text_color="black",hover_color="green",width=50,corner_radius=25,
                        font=("helvetica",15))
        pl_b3.place(x=560,y=300)

        pl_b4=ct.CTkButton(self,text="--",command=deletesong,
                        text_color="black",hover_color="green",width=50,corner_radius=25,
                        font=("helvetica",15))
        pl_b4.place(x=630,y=300)

    def display(self,songs=True):
        if songs:
            self.tree2.delete(*self.tree2.get_children())
            for i in range(len(self.songs)):
                t=self.songs[i]
                self.tree2.insert("","end",values=t)
        else:
            self.tree1.delete(*self.tree1.get_children())
            for i in range(len(self.playlists)):
                t=self.playlists[i]
                self.tree1.insert("","end",values=t)
        
         
    def clear(self):
        self.tree2.destroy()    
    """
    def save(self):
        for temp in self.playlists:
            #db.add_data(temp)
            pass
        
        
        #db.clear_table(self.playlist)
        self.destroy()
        for temp in self.songs:
            #db.add_data(temp,name=self.playlist,playlist=False)    
            pass
        print(self.songs,self.playlists,sep="\n")"""
    def run(self):
        self.main_window()
        #self.protocol("WM_DELETE_WINDOW",self.save)
        self.mainloop()



obj=app()
obj.run()       