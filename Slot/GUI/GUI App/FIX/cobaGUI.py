import tkinter as tk
import os
from os import listdir
from os.path import isfile, join
from tkinter import filedialog
from tkinter import ttk
from PIL import ImageTk
from PIL.ImageTk import PhotoImage
from pendeteksian import *
from gifPlay import MyLabel
import sys
#======================================================================

coordinateDict = {'Dummy','Masih dummy','Dummy lagi'}

rowLabel = {}
rowEntry = {}
row = 0
rowValue = 0
panelA = None
panelB = None
path = ''
ROISlot = []
anim = None

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
        global container,frame,frames
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
        frame = Frame1(container, self)

        # initializing frame of that object from
        # startpage, page1, page2 respectively with
        # for loop
        self.frames[Frame1] = frame

        frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(Frame1)

    def refresh_frame(self,cont):
        frame = cont(container,self)
        self.frames[cont] = frame
        frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(cont)


    #print(frames)
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
                        command = lambda : controller.refresh_frame(Frame2))
        f1Btn2 = tk.Button(self, text='Deteksi Slot', width=20, height=2, font=("Helvetica 10 bold"), command = lambda : controller.refresh_frame(Frame6))

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
        print(rowValue)


    def __init__(self, parent, controller):
        global row, rowLabel, rowEntry
        row = 0
        rowLabel = {}
        rowEntry = {}
        tk.Frame.__init__(self, parent)
        f2Btn1 = tk.Button(self, text='Back', padx=10, pady=10, fg='black', height=1, width=5,
                        font=("Helvetica 10 bold"), command = lambda : controller.show_frame(Frame1))
        f2Label1 = tk.Label(self, text="Masukkan jumlah slot parkir pada setiap barisnya", padx=10, pady=10,
                         font=('Helvetica 12 bold'))

        f2Btn2 = tk.Button(self, text='Hapus baris', padx=10, pady=10, fg='black', height=1, width=10,
                        font=("Helvetica 10 bold"), command=self.delRow)
        f2Btn3 = tk.Button(self, text='Tambah baris', padx=10, pady=10, fg='black', height=1, width=10,
                        font=("Helvetica 10 bold"), command=self.addRow)

        f2Btn4 = tk.Button(self, text='Berikutnya', padx=10, pady=10, fg='black', height=1, width=15,
                        font=("Helvetica 10 bold"), command = lambda : [self.storeValue(), controller.refresh_frame(Frame3)])

        f2Btn1.grid(row=0, column=0, padx=10, pady=10, ipady=1, ipadx=5)
        f2Label1.grid(row=1, column=0, columnspan=4, padx=6, pady=6)
        f2Btn2.grid(row=2, column=0, padx=8, pady=8,ipady=1, ipadx=10)
        f2Btn3.grid(row=2, column=1, padx=8, pady=8, ipady=1, ipadx=10)
        f2Btn4.grid(row=13, column=1, padx=8, pady=8, ipady=1, ipadx=15)

class Frame3(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        f3Btn1 = tk.Button(self, text='Back', padx=10, pady=10, fg='black', height=1, width=5,
                        font=("Helvetica 10 bold"),command = lambda : controller.refresh_frame(Frame2))
        f3Label1 = tk.Label(self, text="Silahkan melakukan inisialisasi slot \ndengan klik kiri pada ujung slot \nseperti contoh berikut", padx=10, pady=10,
                         font=('Helvetica 12 bold'))
        f3Label2 = tk.Label(self, text="Apabila terdapat salah klik, klik \nkanan mouse untuk kembali \nTekan c untuk ke baris selanjutnya", padx=10,
                         pady=10, font=('Helvetica 12 bold'))


        f3Btn2 = tk.Button(self, text='Upload gambar', padx=10, pady=10, fg='black', height=1, width=15,
                        font=("Helvetica 10 bold"), command=select_image)

        f3Btn3 = tk.Button(self, text='Berikutnya', padx=10, pady=10, fg='black', height=1, width=15,
                        font=("Helvetica 10 bold"), command=lambda : controller.refresh_frame(Frame4))

                    

        f3Btn1.grid(row=0, column=0, padx=10, pady=10, ipady=1, ipadx=5)

        f3Btn1.grid(row=0, column=0, padx=10, pady=10)

        f3Label1.grid(row=1, column=0, columnspan=2, padx=6, pady=6)
        f3Label2.grid(row=3, column=0, columnspan=2, padx=6, pady=6)


        f3Btn2.grid(row=3, column=2, padx=10, pady=10, ipady=1, ipadx=5)
        f3Btn3.grid(row=3, column=3, padx=10, pady=10, ipady=1, ipadx=5)

        anim = MyLabel(self, 'assets/gifz.gif')
        #anim.pack()

        anim.grid(row=1, column=2, padx=10, pady=10, columnspan=1)

        

class Frame4(tk.Frame):
    def getROISlot(self):
        global ROISlot
        ROISlot = Detection.inisialisasi(self,path,rowValue)
        self.f4Label1['text'] = 'INISIALISASI SELESAI'
    def saveKoordinat(self):
        global namaFile
        arr = np.array(ROISlot, dtype=object)
        namaFile = self.f4Entry1.get()
        save("data/"+str(namaFile)+".npy", arr)
        #np.save("data/"+str(namaFile)+".npy",arr)
        print('END')

    def clear(self):
        rowLabel = {}
        rowEntry = {}
        row = 0

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        f4Btn1 = tk.Button(self, text='Back', padx=10, pady=10, fg='black', height=1, width=5,
                        font=("Helvetica 10 bold"),command = lambda : controller.refresh_frame(Frame3))
        f4Btn2 = tk.Button(self, text='Mulai', padx=10, pady=10, fg='black', height=1, width=15,
                        font=("Helvetica 10 bold"), command = self.getROISlot)
        f4Btn3 = tk.Button(self, text='Selesai', padx=10, pady=10, fg='black', height=1, width=15,
                        font=("Helvetica 10 bold"), command= lambda : [self.saveKoordinat(), self.clear(), controller.refresh_frame(Frame5)])
        
        self.f4Label1 = tk.Label(self, text='Silahkan untuk mulai inisialisasi', padx=10,
                         pady=10, font=('Helvetica 12 bold')) 
        f4Label2 = tk.Label(self, text="Nama area observasi = ", padx=10,
                         pady=10, font=('Helvetica 12 bold'))  
        self.f4Entry1 = tk.Entry(self, bd=5)                                               
        f4Btn1.grid(row=0,column=0, padx=8, pady=8, ipady=1, ipadx=15)
        self.f4Label1.grid(row=1,column=2,columnspan=4, padx=8, pady=8, ipady=1, ipadx=15)
        f4Label2.grid(row=4,column=1,columnspan=4, padx=8, pady=8, ipady=1, ipadx=15)
        f4Btn2.grid(row=3, column=3, padx=8, pady=8, ipady=1, ipadx=15)
        f4Btn3.grid(row=5, column=3, padx=8, pady=8, ipady=1, ipadx=15)
        self.f4Entry1.grid(row=4,column=5,columnspan=2, padx=8, pady=8, ipady=1, ipadx=15)

class Frame5(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        f5Label1 = tk.Label(self, text="Koordinat slot parkir dengan nama " + namaFile +"\ntelah berhasil disimpan.",padx=10,pady=10,font=('Helvetica 14 bold'))
        f5Label2 = tk.Label(self, text="Apakah anda ingin melakukan inisialisasi area parkir lainnya?",padx=10,pady=10,font=('Helvetica 14 bold'))
        f5Btn1 = tk.Button(self, text='Ya', padx=10, pady=10, fg='black', height=1, width=8, font=("Helvetica 10 bold"), command = lambda : controller.refresh_frame(Frame2))
        f5Btn2 = tk.Button(self, text='Tidak', padx=10, pady=10, fg='black', height=1, width=8, font=("Helvetica 10 bold"), command = lambda : controller.refresh_frame(Frame6))

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
        NewCoordineteDict = [i[:-4] for i in coordinateDict]

        print(NewCoordineteDict)

        #os.chdir(curdir+)

        tk.Frame.__init__(self, parent)

        f6Btn1 = tk.Button(self, text='Back', padx=10, pady=10, fg='black', height=1, width=5,
                            font=("Helvetica 10 bold"), command = lambda : controller.refresh_frame(Frame1))
        f6Label1 = tk.Label(self, text="Silahkan pilih area observasi", padx=10, pady=10,
                             font=('Helvetica 14 bold'))

        value_inside = tk.StringVar(self)
        value_inside.set("Select an Option")

        f6DropDown = tk.OptionMenu(self, value_inside, *NewCoordineteDict)
        #f6DropDown.pack()

        #anim = MyLabel(tk.Frame, 'gifz.gif')
        #anim.pack()

        def get_coordinate():
            global coordinatePath

            coordinate = value_inside.get()
            coordinatePath = curdir + "\\" + coordinate + ".npy"
            print("Cek:"+coordinatePath)

            return None

        f6Btn2 = tk.Button(self, text='Upload gambar', padx=10, pady=10, fg='black', height=1, width=15,
                            font=("Helvetica 10 bold"),command = select_image)


        f6Btn3 = tk.Button(self, text='Berikutnya', padx=25, pady=10, fg='black', height=1, width=15,
                            font=("Helvetica 10 bold"), command = lambda : [get_coordinate(), controller.refresh_frame(Frame7)])

        f6Btn1.grid(row=0, column=0, padx=10, pady=10)
        f6Label1.grid(row=1, column=0, columnspan=4, padx=10, pady=15)
        f6DropDown.grid(row=2, column=0, rowspan=2, padx=10, pady=15)
        f6Btn2.grid(row=5, column=1, pady=20, padx=10)
        f6Btn3.grid(row=5, column=2, pady=20, padx=25)


class Frame7(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        global inputText, outputText
        global slot1Text, slot2Text, slot3Text, slot1Result, slot2Result, slot3Result
        global panelA, panelB, plottedImage, image

        btn = tk.Button(self, text="Home", command= lambda : [controller.show_frame(Frame1)])
        btn.grid(row=3, column=7, padx='10', pady='10')

        btn2 = Button(self, text="Exit", command=lambda : [sys.exit()])
        btn2.grid(row=3, column=8, padx='10', pady='10')



        self.load()



    def load(self):

        image = cv2.imread(path)

        index, box = Detection.car_detection(self,image)
        outImg, slot2Value, slot3Value = Detection.determine_occupancy(self,indexes=index, box=box, path=path, coordinatePath=coordinatePath)

        screen_width = self.winfo_screenwidth()
        img_width = int((48/100) * screen_width)
        h, w = image.shape[:2]
        r = img_width / float(w)
        dim = (img_width, int(h * r))

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
        #if panelA is None or panelB is None:
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
        slot1Result = tk.Label(self,text='= ' + str(slot2Value + slot3Value), font=('Arial', 14), pady=10, fg='red')
        slot1Result.grid(row=2, column=3)
        # Occupied slot
        slot2Result = tk.Label(self,text='= ' + str(slot2Value), font=('Arial', 14), pady=10, fg='red')
        slot2Result.grid(row=3, column=3)
        # Vacant slot
        slot3Result = tk.Label(self,text='= ' + str(slot3Value), font=('Arial', 14), pady=10, fg='red')
        slot3Result.grid(row=4, column=3)


        # otherwise, update the image panels
        #else:
        # update the pannels
        panelA.configure(image=image)
        panelB.configure(image=plottedImage)
        panelA.image = image
        panelB.image = plottedImage

        # text untuk hasil slot (total, occupied, dan vacant)
        # Total slot
        slot1Result = tk.Label(self,text='= ' + str(slot2Value + slot3Value), font=('Arial', 14), pady=10, fg='red')
        slot1Result.grid(row=2, column=3)
        # Occupied slot
        slot2Result = tk.Label(self,text='= ' + str(slot2Value), font=('Arial', 14), pady=10, fg='red')
        slot2Result.grid(row=3, column=3)
        # Vacant slot
        slot3Result = tk.Label(self,text='= ' + str(slot3Value), font=('Arial', 14), pady=10, fg='red')
        slot3Result.grid(row=4, column=3)


# run the GUI
app = tkinterApp()
app.title('Smart Parking System V1.0')
app.mainloop()