import os
from tkinter import*
import tkinter.messagebox
from tkinter import filedialog
from pygame import mixer
from mutagen.mp3 import MP3
root=Tk()

root.title("MY MP3 Player")

root.iconbitmap(r'favicon.ico')

mixer.init()    #initializing the mixer

#Global Declarations
pathlist = []
index = 0
paused = False

#Add Song Function
def add_song():
    global pathlist
    pathlist=filedialog.askopenfilenames(title= "Choose a song" , filetypes=(("mp3 files","*.mp3"),))
    for song in pathlist:
        song = os.path.basename(song)      #to remove the path  from song name
        song = song.replace(".mp3",'')          #to remove .mp3 from song name
        song_box.insert(END,song)              #insert in listbox

#Play Song
def play():
    song = song_box.get(ACTIVE)
    statusbar['text'] = "Playing Music" + ' ' + song
    for i in pathlist:
        if song in i:
            song=i
            break
    try:
        mixer.music.load(song)
        mixer.music.play(loops=0)
        show_details(song)
    except:
        tkinter.messagebox.showerror("File not found", "Music Player could not find the file. Please Check Again")

#Stop Music
def stop():
    try:
        mixer.music.stop()
        song_box.selection_clear(ACTIVE)
        statusbar['text'] = "Music is Stopped"
    except:
        tkinter.messagebox.showerror("File not found", "Music Player could not find the file. Please Check Again")

#Pause Current Playing Song
def pause(is_paused):
    global paused
    paused = is_paused
    if paused:
        mixer.music.unpause()    #to unpause paused song
        paused = False
        song = song_box.get(ACTIVE)
        statusbar['text']="Playing Music" + ' ' + song
    else:
        mixer.music.pause()          #to pause song
        paused = True
        statusbar['text'] = "Music is Paused"

#Play Next Song
def next_song():
    global index,pathlib
    next_one = song_box.curselection()

    #Add one to the song no.
    try:
        index = next_one[0]+1
    except IndexError:
        index +=1
    if len(pathlist)==index:
        index=0
    song = song_box.get(index)  #get next song from the listbox
    for i in pathlist:                              #add path to the song name
        if song in i:
            song=i
            break
    try:
        #Play song
        mixer.music.load(song)
        mixer.music.play(loops=0)
        show_details(song)
        #To clear active bar
        song_box.selection_clear(ACTIVE)

        #To Activate New song bar
        song_box.activate(index)

        #Set Active Bar to next Song
        song_box.selection_set(index,last=None)
    except:
        tkinter.messagebox.showerror("File not found", "Music Player could not find the file. Please Check Again")
        
#Play Previous Song
def pre_song():
    global index, pathlib
    prev = song_box.curselection()
   
    #Add one to the song no.
    try:
        index = prev[0]-1
    except IndexError:
        index -=1
    if index==(-1):
        index=len(pathlist)-1
    song = song_box.get(index)  #get next song from the listbox
    for i in pathlist:                              #add path to the song name
        if song in i:
            song=i
            break
    try:
        #Play song
        mixer.music.load(song)
        mixer.music.play(loops=0)
        show_details(song)
        #To clear active bar
        song_box.selection_clear(ACTIVE)

        #To Activate New song bar
        song_box.activate(index)

        #Set Active Bar to next Song
        song_box.selection_set(index,last=None)
    except:
        tkinter.messagebox.showerror("File not found", "Music Player could not find the file. Please Check Again")

def set_vol(val):
    volume=int(val)/100
    mixer.music.set_volume(volume)
    # Set_Volume of mixer takes value only from 0 to 1.

muted=FALSE

def mute_music():
    global muted
    if muted:    #unmute the music
        mixer.music.set_volume(0.75)
        volumebtn.configure(image=volumephoto)
        scale.set(75)
        muted = FALSE
    else:        #Mute the music
        mixer.music.set_volume(0)
        volumebtn.configure(image=mutephoto)
        scale.set(0)
        muted=TRUE

def show_details(play_song):
    total_length=0
    file_data = os.path.splitext(play_song)
    
    if file_data[1] == '.mp3':
        audio = MP3(play_song)
        total_length = audio.info.length
    else:
        a = mixer.Sound(play_song)
        total_length = a.get_length()

    hrs = total_length / 3600
    total_length %= 3600
    mins = total_length / 60
    secs = total_length % 60
    time_format = '{:02d}:{:02d}:{:02d}'.format(round(hrs), round(mins), round(secs))
    lengthlabel['text'] = "Total Length " + ' - ' + time_format


def DELETE():
    global pathlist, index
    selected_song = song_box.curselection()
    selected_song = int(selected_song[0])
    song_box.delete(selected_song)
    pathlist=list(pathlist)
    index-=1
    song = song_box.get(ACTIVE)
    for i in range(len(pathlist)):
        if song in pathlist[i]:
            next_song()
    pathlist.pop(selected_song)

def about():
    tkinter.messagebox.showinfo('About Music Player','This is a music player build in python ')

    
#Create Menu
my_menu=Menu(root)
root.config(menu=my_menu)

#Add SubmenuMenu
sub_menu = Menu(my_menu,tearoff=0,relief=RAISED)
my_menu.add_cascade(label="File",menu=sub_menu)
sub_menu.add_command(label="Open", command=add_song)
sub_menu.add_command(label="Exit", command=root.destroy)

sub_menu = Menu(my_menu,tearoff=0,relief=RAISED)
my_menu.add_cascade(label="Help",menu=sub_menu)
sub_menu.add_command(label="About Us", command=about)


#Top Label
toplabel=Label(root,text='MY MP3 Player',bg='gold',fg='indigo',font='comicsansms 15 italic')
toplabel.pack(side=TOP,fill=X)

#Frames
leftframe=Frame(root)
leftframe.pack(side=LEFT)

rightframe=Frame(root)
rightframe.pack()

topframe=Frame(rightframe)
topframe.pack()

middleframe=Frame(rightframe)
middleframe.pack(pady=30,padx=30)

bottomframe=Frame(rightframe)
bottomframe.pack()

lastframe=Frame(leftframe)
lastframe.grid(row=2)


lengthlabel=Label(middleframe,text="Total Length - 00:00:00" )
lengthlabel.grid(row=0,column=1)

#Control Buttons
playphoto = PhotoImage(file='play.png')
playbtn = Button(middleframe,image= playphoto,command=play,borderwidth=0.1)
playbtn.grid(row=2,column=0,padx=10,pady=40)

pausephoto=PhotoImage(file='pause.png')
pausebtn = Button(middleframe,image= pausephoto,command=lambda:pause(paused),borderwidth=0.1)
pausebtn.grid(row=2,column=1,padx=10,pady=40)

stopphoto=PhotoImage(file='stop.png')
stopbtn = Button(middleframe,image= stopphoto,command=stop,borderwidth=0.1)
stopbtn.grid(row=2,column=2,padx=10,pady=40)

prevphoto=PhotoImage(file='previous.png')
prevbtn = Button(bottomframe,image= prevphoto,command=pre_song,borderwidth=0.1)
prevbtn.grid(row=0,column=0,padx=5)

nextphoto=PhotoImage(file='next.png')
nextbtn = Button(bottomframe,image=nextphoto,command=next_song,borderwidth=0.1)
nextbtn.grid(row=0,column=1,padx=5)

mutephoto=PhotoImage(file='mute.png')
volumephoto=PhotoImage(file='volume.png')
volumebtn = Button(bottomframe,image= volumephoto,command=mute_music,borderwidth=0.1)
volumebtn.grid(row=0,column=2,padx=20)

scale = Scale(bottomframe,from_=0,to=100,orient=HORIZONTAL,command=set_vol)
scale.set(75)       #Implement the default volume when music player start
mixer.music.set_volume(0.75)
scale.grid(row=0,column=3,pady=15)

statusbar = Label(root,text="Welcome to Music Player",relief=SUNKEN,font='Times 12 bold')
statusbar.pack(side=BOTTOM,fill=X)

#Playlist List Box
song_box= Listbox(leftframe,bg='#fff',fg="#c40b13",width=50 , height=26,selectforeground='white',selectbackground='red')
song_box.grid(pady=20,padx=30,row=1,column=0)

addbtn=Button(lastframe,command=add_song,text='Add',width=20,height=2,relief=GROOVE)
addbtn.grid(row=2,column=0)
addbtn=Button(lastframe,command=DELETE,text='Delete',width=20,height=2,relief=GROOVE)
addbtn.grid(row=2,column=1)

def close():
    stop_music()
    root.destroy()
root.protocol("WM_WINDOW_DELETE",close)

root.mainloop()