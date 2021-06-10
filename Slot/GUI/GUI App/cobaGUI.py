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
import os
from pendeteksian import Detection
#======================================================================

coordinateDict = {'Dummy','Masih dummy','Dummy lagi'}
row = 0
rowLabel = {}
rowEntry = {}
panelA = None
panelB = None
rowValue = []

def select_image():
    global path
    # grab a reference to the image panels
    # open a file chooser dialog and allow the user to select an input
    # image
    path = filedialog.askopenfilename()

    print(path) 

class tkinterApp(tk.Tk):

    # __init__ function for class tkinterApp
    def __init__(self, *args, **kwargs):
        # __init__ function for class Tk
        tk.Tk.__init__(self, *args, **kwargs)

        # creating a container
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # initializing frames to an empty array
        self.frames = {}

        # iterating through a tuple consisting
        # of the different page layouts
        for F in (Frame1, Frame2, Frame3, Frame4, Frame5, Frame6, Frame7):
            frame = F(container, self)

            # initializing frame of that object from
            # startpage, page1, page2 respectively with
            # for loop
            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(Frame1)

    # to display the current frame passed as
    # parameter
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

class Frame1(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        f1LabelJudul = tk.Label(self, text='Aplikasi Pendeteksi Status Slot Parkir', padx=10, pady=10, fg='black',
                             height=2, width=50, font=("Helvetica 16 bold"))
        f1Label1 = tk.Label(self, text='Silahkan pilih menu yang diinginkan', padx=10, pady=10, fg='black', height=3,
                         font=("Helvetica 14 bold"))
        f1Btn1 = tk.Button(self, text='Inisialisasi Slot', width=20, height=2, font=("Helvetica 10 bold"),
                        command = lambda : controller.show_frame(Frame2))
        f1Btn2 = tk.Button(self, text='Deteksi Slot', width=20, height=2, font=("Helvetica 10 bold"), command = lambda : controller.show_frame(Frame6))

        f1LabelJudul.grid(row=0, column=1, columnspan=2)
        f1Label1.grid(row=1, column=1, columnspan=2)
        f1Btn1.grid(row=2, column=1, pady=10)
        f1Btn2.grid(row=2, column=2, pady=10)

class Frame2(tk.Frame): 
    def addRow(self):
        global row,rowLabel,rowEntry
        if row == 10:
            return None
        row = row + 1
        rowLabel["%s"%row] = Label(self,text='Jumlah slot baris ke-'+str(row)+'=',padx=10,pady=10,font=('Helvetica 10 bold'))
        rowEntry["%s"%row] = Entry(self,bd=5)

        rowLabel["%s"%row].grid(row=row+2,column=0)
        rowEntry["%s"%row].grid(row=row+2,column=1)

    def delRow(self):
        global row,rowLabel,rowEntry
        if row == 0 :
            return None
        rowLabel["%s"%row].destroy()
        rowEntry["%s"%row].destroy()
        del rowLabel["%s"%row]
        del rowEntry["%s"%row]
        row = row - 1 

    def storeValue(self):
        global rowValue,rowEntry
        rowValue = [] 
        for i in range(len(rowEntry)):
            rowValue.append(int(rowEntry["%s"%(i+1)].get()))
        if len(rowValue) != 0:
            self.f2Btn4["state"] = tk.NORMAL
        else:
            self.f2Btn4["state"] = tk.DISABLED    
        print(rowValue)


    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        f2Btn1 = tk.Button(self, text='Back', padx=10, pady=10, fg='black', height=1, width=5,
                        font=("Helvetica 10 bold"))
        f2Label1 = tk.Label(self, text="Masukkan jumlah slot parkir pada setiap barisnya", padx=10, pady=10,
                         font=('Helvetica 12 bold'))

        f2Btn2 = tk.Button(self, text='Hapus baris', padx=10, pady=10, fg='black', height=1, width=10,
                        font=("Helvetica 10 bold"), command=self.delRow)
        f2Btn3 = tk.Button(self, text='Tambah baris', padx=10, pady=10, fg='black', height=1, width=10,
                        font=("Helvetica 10 bold"), command=self.addRow)

        self.f2Btn4 = tk.Button(self, text='Berikutnya', padx=10, pady=10, fg='black', height=1, width=15,
                        font=("Helvetica 10 bold"), command = lambda : controller.show_frame(Frame3))
        f2Btn5 = tk.Button(self, text='✓', padx=10, pady=10, fg='green', height=1, width=15,
                        font=("Helvetica 10"), command = self.storeValue)

        self.f2Btn4['state'] = tk.DISABLED

        f2Btn1.grid(row=0, column=0, padx=10, pady=10, ipady=1, ipadx=5)
        f2Label1.grid(row=1, column=0, columnspan=4, padx=6, pady=6)
        f2Btn2.grid(row=2, column=0, padx=8, pady=8,ipady=1, ipadx=10)
        f2Btn3.grid(row=2, column=1, padx=8, pady=8, ipady=1, ipadx=10)
        self.f2Btn4.grid(row=13, column=1, padx=8, pady=8, ipady=1, ipadx=15)
        f2Btn5.grid(row=13, column=0, padx=8, pady=8, ipady=1, ipadx=15)

class Frame3(tk.Frame):
    def getRowValue(self):
        global rowValue
        print(rowValue)

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        f3Btn1 = tk.Button(self, text='Back', padx=10, pady=10, fg='black', height=1, width=5,
                        font=("Helvetica 10 bold"),command = lambda : controller.show_frame(Frame2))
        f3Label1 = tk.Label(self, text="Silahkan melakukan inisialisasi\nslot seperti contoh berikut", padx=10, pady=10,
                         font=('Helvetica 12 bold'))
        f3Label2 = tk.Label(self, text="Apabila terdapat salah klik, klik \nkanan mouse untuk kembali ke awal baris", padx=10,
                         pady=10, font=('Helvetica 12 bold'))


        f3Btn2 = tk.Button(self, text='Upload gambar', padx=10, pady=10, fg='black', height=1, width=15,
                        font=("Helvetica 10 bold"))

        f3Btn3 = tk.Button(self, text='Berikutnya', padx=10, pady=10, fg='black', height=1, width=15,
                        font=("Helvetica 10 bold"), command = lambda : controller.show_frame(Frame4))                

        f3Btn1.grid(row=0, column=0, padx=10, pady=10, ipady=1, ipadx=5)

        f3Btn1.grid(row=0, column=0, padx=10, pady=10)

        f3Label1.grid(row=1, column=0, columnspan=2, padx=6, pady=6)
        f3Label2.grid(row=3, column=0, columnspan=2, padx=6, pady=6)
        #anim.grid(row=1, column=2, padx=10, pady=10)


        f3Btn2.grid(row=3, column=2, padx=10, pady=10, ipady=1, ipadx=5)
        f3Btn3.grid(row=3, column=3, padx=10, pady=10, ipady=1, ipadx=5)

        canvas = Canvas(self, width = 200, height = 200)
        canvas.grid(row=1,column=2)
        gifFile = PhotoImage(file="C:\\Users\\LENOVO\\ParkingSlot\\Slot\\GUI\\GUI App\\gifz.gif")
        canvas.create_image(0,0, anchor = NW, image=gifFile)

class Frame4(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        #f4Btn1 = tk.Button(self, text='Back', padx=10, pady=10, fg='black', height=1, width=5,
                        #font=("Helvetica 10 bold"),command = lambda : controller.show_frame(Frame3))

        f4Btn2 = tk.Button(self, text='Berikutnya', padx=10, pady=10, fg='black', height=1, width=15,
                        font=("Helvetica 10 bold"), command = lambda : controller.show_frame(Frame5))

        f4Btn2.grid(row=4, column=1, padx=8, pady=8, ipady=1, ipadx=15)

class Frame5(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        f5Label1 = tk.Label(self, text="Koordinat slot parkir dengan nama #namaareaobservasi\ntelah berhasil disimpan.",padx=10,pady=10,font=('Helvetica 14 bold'))
        f5Label2 = tk.Label(self, text="Apakah anda ingin melakukan inisialisasi area parkir lainnya?",padx=10,pady=10,font=('Helvetica 14 bold'))
        f5Btn1 = tk.Button(self, text='Ya', padx=10, pady=10, fg='black', height=1, width=8, font=("Helvetica 10 bold"), command = lambda : controller.show_frame(Frame2))
        f5Btn2 = tk.Button(self, text='Tidak', padx=10, pady=10, fg='black', height=1, width=8, font=("Helvetica 10 bold"), command = lambda : controller.show_frame(Frame6))

        f5Label1.grid(row=0,column=0,columnspan=4,padx=15,pady=15)
        f5Label2.grid(row=1,column=0,columnspan=4,padx=15,pady=15)
        f5Btn1.grid(row=2,column=1,padx=15,pady=15)
        f5Btn2.grid(row=2,column=2,padx=15,pady=15)


class Frame6(tk.Frame):
    def __init__(self, parent, controller):

        curdir = os.getcwd()+"\data"
        print(curdir)
        print(os.listdir(curdir))
        coordinateDict = os.listdir(curdir)
        #os.chdir(curdir+)

        tk.Frame.__init__(self, parent)

        f6Btn1 = tk.Button(self, text='Back', padx=10, pady=10, fg='black', height=1, width=5,
                            font=("Helvetica 10 bold"), command = lambda : controller.show_frame(Frame1))
        f6Label1 = tk.Label(self, text="Silahkan pilih area observasi", padx=10, pady=10,
                             font=('Helvetica 14 bold'))

        value_inside = tk.StringVar(self)
        value_inside.set("Select an Option")

        #f6DropDown = tk.OptionMenu(self, value_inside, *coordinateDict)
        #f6DropDown.pack()

        #anim = MyLabel(tk.Frame, 'gifz.gif')
        #anim.pack()

        def get_coordinate():
            global coordinate
            coordinate = value_inside.get()
            return None

        submit_button = tk.Button(self, text='Submit', command=lambda :[get_coordinate(), controller.show_frame(Frame7)])


        f6Btn2 = tk.Button(self, text='Upload gambar', padx=10, pady=10, fg='black', height=1, width=15,
                            font=("Helvetica 10 bold"),command = select_image)


        f6Btn3 = tk.Button(self, text='Berikutnya', padx=25, pady=10, fg='black', height=1, width=15,
                            font=("Helvetica 10 bold"), command = lambda : controller.show_frame(Frame1))

        f6Btn1.grid(row=0, column=0, padx=10, pady=10)
        f6Label1.grid(row=1, column=0, columnspan=4, padx=10, pady=15)
        #f6DropDown.grid(row=2, column=0, rowspan=2, padx=10, pady=15)
        f6Btn2.grid(row=5, column=1, pady=20, padx=10)
        f6Btn3.grid(row=5, column=2, pady=20, padx=25)
        submit_button.grid(row=5, column=3, pady=20, padx=25)


class Frame7(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        global inputText, outputText
        global slot1Text, slot2Text, slot3Text, slot1Result, slot2Result, slot3Result
        global panelA, panelB, edged, image

        try:
            image = cv2.imread("C:/Users/ujang/Desktop/sampel gambar/SUNNY/camera8.jpg")

            index, box = Detection.car_detection(self,image)
            outImg = Detection.determine_occupancy(self,indexes=index, box=box)

            scale_percent = 65  # percent of original size
            width = int(image.shape[1] * scale_percent / 100)
            height = int(image.shape[0] * scale_percent / 100)
            dim = (width, height)

            # resize image
            resized_image = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
            resized_plot = cv2.resize(outImg, dim, interpolation=cv2.INTER_AREA)

            resized_image = cv2.cvtColor(resized_image, cv2.COLOR_BGR2RGB)
            resized_plot = cv2.cvtColor(resized_plot, cv2.COLOR_BGR2RGB)

            # convert the images to PIL format...
            image = Image.fromarray(resized_image)
            plottedImage = Image.fromarray(resized_plot)
            # ...and then to ImageTk format
            image = ImageTk.PhotoImage(image)
            plottedImage = ImageTk.PhotoImage(plottedImage)

            # if the panels are None, initialize them
            if panelA is None or panelB is None:
                # text 'Gambar input'
                inputText = tk.Label(self,text='Input', font=('Arial', 20), pady=5)
                inputText.grid(row=0, column=0)
                # text 'Gambar output'
                outputText = tk.Label(self,text='            Output', font=('Arial', 20), pady=5)
                outputText.grid(row=0, column=6)

                # the first panel will store our original image
                panelA = tk.Label(self,image=image)
                panelA.image = image
                # panelA.pack(side="left", padx=10, pady=10)
                panelA.grid(row=1, column=0, columnspan=6, padx='10', pady='10')

                # while the second panel will store the edge map
                panelB = tk.Label(self,image=plottedImage)
                panelB.image = plottedImage
                # panelB.pack(side="right", padx=10, pady=10)
                panelB.grid(row=1, column=6, columnspan=6, padx='10', pady='10')

                # text untuk keterangan slot (total, occupied, dan vacant)
                # Total slot
                slot1Text = tk.Label(self,text='Total lahan parkir      ', font=('Arial', 14), pady=5)
                slot1Text.grid(row=2, column=1)
                # Occupied slot
                slot2Text = tk.Label(self,text='Lahan parkir terisi    ', font=('Arial', 14), pady=5)
                slot2Text.grid(row=3, column=1)
                # Vacant slot
                slot3Text = tk.Label(self,text='Lahan parkir kosong', font=('Arial', 14), pady=5)
                slot3Text.grid(row=4, column=1)

                # text untuk hasil slot (total, occupied, dan vacant)
                # Total slot
                slot1Result = tk.Label(self,text='= ' + str("slot2Value" + "slot3Value"), font=('Arial', 14), pady=10, fg='red')
                slot1Result.grid(row=2, column=3)
                # Occupied slot
                slot2Result = tk.Label(self,text='= ' + str("slot2Value"), font=('Arial', 14), pady=10, fg='red')
                slot2Result.grid(row=3, column=3)
                # Vacant slot
                slot3Result = tk.Label(self,text='= ' + str("slot3Value"), font=('Arial', 14), pady=10, fg='red')
                slot3Result.grid(row=4, column=3)


            # otherwise, update the image panels
            else:
                # update the pannels
                panelA.configure(image=image)
                panelB.configure(image=plottedImage)
                panelA.image = image
                panelB.image = plottedImage

                # text untuk hasil slot (total, occupied, dan vacant)
                # Total slot
                slot1Result = tk.Label(self,text='= ' + str("slot2Value" + "slot3Value"), font=('Arial', 14), pady=10, fg='red')
                slot1Result.grid(row=2, column=3)
                # Occupied slot
                slot2Result = tk.Label(self,text='= ' + str("slot2Value"), font=('Arial', 14), pady=10, fg='red')
                slot2Result.grid(row=3, column=3)
                # Vacant slot
                slot3Result = tk.Label(self,text='= ' + str("slot3Value"), font=('Arial', 14), pady=10, fg='red')
                slot3Result.grid(row=4, column=3)


                btn = tk.Button(self, text="Pilih gambar input", command=select_image)
                btn.grid(row=3, column=7, padx='10', pady='10')
                btn.pack(side="bottom", fill="both", expand="yes", padx="10", pady="10")

        except:
            print("error")
# kick off the GUI

global anim



app = tkinterApp()
app.mainloop()