#!/usr/bin/python3

import youtube_dl
import sys, os
from tkinter import *
import tkinter.messagebox as tmb
try:
    import pyperclip
except ModuleNotFoundError:
    paste_event = False
else:
    paste_event = True

root = Tk()
root.title("[Gemate Gtk]")

menu_bar = Menu(root)
pas = None

#variables
pastes = StringVar()
ticked = IntVar()

#commands and callbacks
def download():
    print(ticked.get())
    url = pastes.get()
    ydl_opts={}
    if not url:
        tmb.showwarning(title="NO URL", message="Please Provide A URL")
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    
def manual():
    man_text = "A Tool for downloading Youtube videos and audios, and also from other sites as well. Just copy the url of the video and paste it, Choose your file format then hit download"
    tmb.showinfo(title="Manual", message=man_text)

def paste():
    if paste_event:
        past = pyperclip.paste()
        pastes.set(past)
def show_popup(event):
    popup.tk_popup(event.x_root, event.y_root)

file = Menu(menu_bar, tearoff=0)
files = menu_bar.add_cascade(label="File", menu=file)
file.add_command(label="New", accelerator="Ctrl+N", underline=0)

about = Menu(menu_bar, tearoff=0)
abouts = menu_bar.add_cascade(label="About", menu=about)
about.add_command(label="About")

helps = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Help", menu=helps)
helps.add_command(label="Manpage", command=manual, accelerator='F1')

extra = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label='Extras', menu=extra)
extra.add_command(label="Supported Sites")


Label(root, text="Tool for downloading Videos", font='{nimbus roman} 20 bold italic', foreground='light sea green').grid(row=1, column=1)

ent=Entry(root, width=40, textvariable=pastes).grid(row=3, column=1, sticky='w')
Label(root, text="Enter the Video url:").grid(row=3, column=0, sticky='w')
Radiobutton(root, variable=ticked, value=1).grid(row=6, column=0,sticky='e')
Radiobutton(root, variable=ticked, value=2).grid(row=5, column=0,sticky='e')
Button(root, text='Download', command=download).grid(row=7, column=2)
Label(root, text='mp3/audio').grid(row=5, column=1, sticky='w')
Label(root, text='mp4/video').grid(row=6, column=1, sticky='w')

ticked.set(2)

popup = Menu(ent)
popup.add_command(label='paste', underline=0, command=paste)

paste()
#ent.bind('<Button-3>', show_popup, add=None)
root.bind_all('<Return>', download)

root.config(menu=menu_bar)
mainloop()
