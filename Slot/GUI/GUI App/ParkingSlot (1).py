from tkinter import font
import cv2
import tkinter as tk
import numpy as np
import math
from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image
from shapely.geometry import Polygon
from PIL.ImageTk import PhotoImage
#======================================================================
global state,frame1,frame2,frame    #Variabel indikator state
#initialize main windows toolkit 
root = Tk()
root.title('Parking Slot App')
#initialize each frame
frame1 = tk.Frame(root)
frame2 = tk.Frame(root)
frame3 = tk.Frame(root)
frame5 = tk.Frame(root)
frame6 = tk.Frame(root)

gifFile = PhotoImage(Image.open('gifz.gif'))
coordinateDict = {'Dummy','Masih dummy','Dummy lagi'}
row = 0
rowLabel = dict()
rowEntry = dict()


class MyLabel(Label):
    def __init__(self, master, filename):
        im = Image.open(filename)
        seq =  []
        try:
            while 1:
                seq.append(im.copy())
                im.seek(len(seq)) # skip to next frame
        except EOFError:
            pass # we're done

        try:
            self.delay = im.info['duration']
        except KeyError:
            self.delay = 100

        first = seq[0].convert('RGBA')
        self.frames = [ImageTk.PhotoImage(first)]

        Label.__init__(self, master, image=self.frames[0])

        temp = seq[0]
        for image in seq[1:]:
            temp.paste(image)
            frame = temp.convert('RGBA')
            self.frames.append(ImageTk.PhotoImage(frame))

        self.idx = 0

        self.cancel = self.after(self.delay, self.play)

    def play(self):
        self.config(image=self.frames[self.idx])
        self.idx += 1
        if self.idx == len(self.frames):
            self.idx = 0
        self.cancel = self.after(self.delay, self.play)

def addRow():
    global row,rowLabel,rowEntry
    if row == 10:
        return None
    row = row + 1
    rowLabel[row] = Label(frame2,text='Jumlah slot baris ke-'+str(row)+'=',padx=10,pady=10,font=('Helvetica 10 bold'))
    rowEntry[row] = Entry(frame2,bd=5)

    rowLabel[row].grid(row=row+2,column=0)
    rowEntry[row].grid(row=row+2,column=1)

def delRow():
    global row,rowLabel,rowEntry
    if row == 0 :
        return None
    rowLabel[row].destroy()
    rowEntry[row].destroy()
    row = row - 1    

def FRAME1():
    f1LabelJudul = Label(frame1, text='Aplikasi Pendeteksi Status Slot Parkir', padx=10, pady=10, fg='black', height=2, width=50, font=("Helvetica 16 bold"))
    f1Label1 = Label(frame1, text='Silahkan pilih menu yang diinginkan', padx=10, pady=10, fg='black', height=3, font=("Helvetica 14 bold"))
    f1Btn1 = Button(frame1, text='Inisialisasi Slot',width=20,height=2, font=("Helvetica 10 bold"))
    f1Btn2 = Button(frame1, text='Deteksi Slot',width=20,height=2, font=("Helvetica 10 bold"))
    f1LabelJudul.grid(row=0, column=1, columnspan=2)
    f1Label1.grid(row=1, column=1, columnspan=2)
    f1Btn1.grid(row=2, column=1, pady=10)
    f1Btn2.grid(row=2, column=2, pady=10)

    frame1.grid(row=0, column=0)

def FRAME2():
    global rowLabel,rowEntry
    f2Btn1 = Button(frame2, text='Back', padx=10, pady=10, fg='black', height=1, width=5, font=("Helvetica 10 bold"))
    f2Label1 = Label(frame2, text="Masukkan jumlah slot parkir pada setiap barisnya",padx=10,pady=10,font=('Helvetica 12 bold'))
    f2Btn2 = Button(frame2, text='Hapus baris', padx=10, pady=10, fg='black', height=1, width=10, font=("Helvetica 10 bold"),command=delRow)
    f2Btn3 = Button(frame2, text='Tambah baris', padx=10, pady=10, fg='black', height=1, width=10, font=("Helvetica 10 bold"),command=addRow)
    f2Btn4 = Button(frame2, text='Berikutnya', padx=10, pady=10, fg='black', height=1, width=15, font=("Helvetica 10 bold"))

    f2Btn1.grid(row=0,column=0,padx=10,pady=10)
    f2Label1.grid(row=1,column=0,columnspan=4,padx=6,pady=6)
    f2Btn2.grid(row=2,column=0,padx=8,pady=8)
    f2Btn3.grid(row=2,column=1,padx=8,pady=8)
    f2Btn4.grid(row=50,column=1,padx=8,pady=8)


    frame2.grid(row=0,column=0)

def FRAME3():
    f3Btn1 = Button(frame3, text='Back', padx=10, pady=10, fg='black', height=1, width=5, font=("Helvetica 10 bold"))
    f3Label1 = Label(frame3, text="Silahkan melakukan inisialisasi\nslot seperti contoh berikut",padx=10,pady=10,font=('Helvetica 12 bold'))
    f3Label2 = Label(frame3, text="Apabila terdapat salah klik, tekan\n'Z' untuk kembali ke awal baris",padx=10,pady=10,font=('Helvetica 12 bold'))
    #gifPanel = Label(frame3, image=gifFile, padx=10, pady=10)
    f3Btn2 = Button(frame3, text='Upload gambar', padx=10, pady=10, fg='black', height=1, width=15, font=("Helvetica 10 bold"))

    f3Btn1.grid(row=0,column=0,padx=10,pady=10)
    f3Label1.grid(row=1,column=0,columnspan=2,padx=6,pady=6)
    f3Label2.grid(row=3,column=0,columnspan=2,padx=6,pady=6)
    #gifPanel.grid(row=1,column=2, padx=10, pady=10)
    f3Btn2.grid(row=3,column=2)

    anim = MyLabel(root, 'gifz.gif')
    #anim.pack()

    anim.grid(row=1, column=2, padx=10, pady=10)

    frame3.grid(row=0,column=0)

def FRAME5():
    f5Label1 = Label(frame5, text="Koordinat slot parkir dengan nama #namaareaobservasi\ntelah berhasil disimpan.",padx=10,pady=10,font=('Helvetica 14 bold'))
    f5Label2 = Label(frame5, text="Apakah anda ingin melakukan inisialisasi area parkir lainnya?",padx=10,pady=10,font=('Helvetica 14 bold'))
    f5Btn1 = Button(frame5, text='Ya', padx=10, pady=10, fg='black', height=1, width=8, font=("Helvetica 10 bold"))
    f5Btn2 = Button(frame5, text='Tidak', padx=10, pady=10, fg='black', height=1, width=8, font=("Helvetica 10 bold"))

    f5Label1.grid(row=0,column=0,columnspan=4,padx=15,pady=15)
    f5Label2.grid(row=1,column=0,columnspan=4,padx=15,pady=15)
    f5Btn1.grid(row=2,column=1,padx=15,pady=15)
    f5Btn2.grid(row=2,column=2,padx=15,pady=15)

    frame5.grid(row=0,column=0)

def FRAME6():
    f6Btn1 = Button(frame6, text='Back', padx=10, pady=10, fg='black', height=1, width=5, font=("Helvetica 10 bold"))
    f6Label1 = Label(frame6, text="Silahkan pilih area observasi",padx=10,pady=10,font=('Helvetica 14 bold'))
    f6DropDown = OptionMenu(frame6, StringVar(), *coordinateDict)
    f6Btn2 = Button(frame6, text='Upload gambar', padx=10, pady=10, fg='black', height=1, width=15, font=("Helvetica 10 bold"))

    f6Btn1.grid(row=0,column=0,padx=10,pady=10)
    f6Label1.grid(row=1,column=0,columnspan=4,padx=10,pady=15)
    f6DropDown.grid(row=2,column=0,rowspan=2,padx=10,pady=15)
    f6Btn2.grid(row=5,column=1,pady=20,padx=10)

    frame6.grid(row=0,column=0)






FRAME3()






root.mainloop()
