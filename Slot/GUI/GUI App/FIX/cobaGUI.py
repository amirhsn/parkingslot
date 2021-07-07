import tkinter as tk
import os
from os import listdir
from os.path import isfile, join
from tkinter import filedialog
from tkinter import ttk
from PIL import ImageTk
from PIL.ImageTk import PhotoImage
from numpy.lib.type_check import imag
from shapely.geometry.polygon import orient
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
    global path, buttonState
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
        screenWidth = self.winfo_screenwidth()
        screenHeight = self.winfo_screenheight()

        background_image = ImageTk.PhotoImage((Image.open('assets/frame1.png')).resize((screenWidth, screenHeight)))
        background_label = tk.Label(self, image=background_image)
        background_label.image = background_image
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        """ logoPolbanImg  = ImageTk.PhotoImage((Image.open('assets/POLBAN.png')).resize((100,100)))
        logoPolban = tk.Label(self, image = logoPolbanImg)
        logoPolban.image = logoPolbanImg
        logoPolban.configure(bg='#585858')

        logoCarImg  = ImageTk.PhotoImage((Image.open('assets/SP-colour.png')).resize((100,100)))
        logoCar = tk.Label(self, image = logoCarImg)
        logoCar.image = logoCarImg
        logoCar.configure(bg='#585858') """

        logoExitImg = ImageTk.PhotoImage((Image.open('assets/exit.png')).resize((80, 80)))
        logoExit = tk.Label(self, image=logoExitImg)
        logoExit.image = logoExitImg

        exitButton = tk.Button(self, image=logoExitImg, borderwidth=0, command=lambda: [sys.exit()])
        exitButton.configure(bg='#3b3b3b')
        """ f1LabelJudul1 = tk.Label(self, text='Aplikasi Pendeteksi \nStatus Slot Parkir', padx=10, fg='white',
                             height=2, width=50, font=("Helvetica 30 bold"))
        f1LabelJudul1.configure(bg='#585858') """
        # f1LabelJudul2 = tk.Label(self, text='Status Slot Parkir', padx=10, fg='#ff6200',
        #                     height=2, width=50, font=("Helvetica 30 bold"))
        # f1Label1 = tk.Label(self, text='Silahkan pilih menu yang diinginkan', padx=10, pady=10, fg='black', height=3,
        #                 font=("Helvetica 14 bold"))
        inisImg = ImageTk.PhotoImage((Image.open('assets/inis.png')).resize((250, 80)))
        inis = tk.Label(self, image=inisImg)
        inis.image = inisImg
        f1Btn1 = tk.Button(self, image=inisImg, font=("Helvetica 20 bold"),
                           command=lambda: controller.refresh_frame(Frame2), bg='#474747', borderwidth=0)                   

        detImg = ImageTk.PhotoImage((Image.open('assets/deteksi.png')).resize((250, 80)))
        det = tk.Label(self, image=detImg)
        det.image = detImg
        f1Btn2 = tk.Button(self, image=detImg, font=("Helvetica 20 bold"),
                           command=lambda: controller.refresh_frame(Frame6), bg='#3f3f3f', borderwidth=0)

        """ logoPolban.grid(row=0, column=0, padx=30, pady=30)
        logoCar.grid(row=0,column=7) """
        exitButton.place(relx=0.83, rely=0.8, anchor=CENTER)

        """ f1LabelJudul1.grid(row=0, column=4, columnspan=2) """
        # f1LabelJudul2.grid(row=1, column=4, columnspan=2)
        # f1Label1.grid(row=1, column=1, columnspan=2)
        f1Btn1.place(relx=0.5, rely=0.5, anchor=CENTER)
        f1Btn2.place(relx=0.5, rely=0.65, anchor=CENTER)

class Frame2(tk.Frame):

    def addRow(self):
        global row,rowLabel,rowEntry
        self.f2Btn4['state'] = NORMAL
        if row == 10:
            return None
        row = row + 1
        rowLabel["%s"%row] = Label(self,text='Jumlah slot baris ke-'+str(row)+'=',padx=10,pady=10,font=('Helvetica 10 bold'), bg='#494949', fg='white')
        rowEntry["%s"%row] = Entry(self,bd=5)

        """ rowLabel["%s"%row].grid(row=row+2,column=2)
        rowEntry["%s"%row].grid(row=row+2,column=3) """
        rowLabel["%s"%row].place(relx=0.30, rely=0.34+(row*0.04), anchor=CENTER)
        rowEntry["%s"%row].place(relx=0.42, rely=0.34+(row*0.04), anchor=CENTER)
    def delRow(self):
        global row,rowLabel,rowEntry
        if row == 1 :
            self.f2Btn4['state'] = DISABLED
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
        screenWidth = self.winfo_screenwidth()
        screenHeight = self.winfo_screenheight()

        background_image= ImageTk.PhotoImage((Image.open('assets/frame2.png')).resize((screenWidth,screenHeight)))
        background_label = tk.Label(self, image=background_image)
        background_label.image = background_image
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        logoBackImg  = ImageTk.PhotoImage((Image.open('assets/back.png')).resize((80,80)))
        logoBack = tk.Label(self, image = logoBackImg)
        logoBack.image = logoBackImg

        backButton = tk.Button(self, image=logoBackImg, bg="#585858", borderwidth=0, command=lambda : controller.show_frame(Frame1))

        #f2Btn1 = tk.Button(self, text='Back', padx=10, pady=10, fg='black', height=1, width=5,
        #                font=("Helvetica 10 bold"), command = lambda : controller.show_frame(Frame1))
        #f2Label1 = tk.Label(self, text="Masukkan jumlah slot parkir\n pada setiap barisnya", padx=10, pady=10,
        #                 font=('Helvetica 30 bold'), bg='#585858', fg='white')

        hapusImg  = ImageTk.PhotoImage((Image.open('assets/hapus.png')).resize((100,40)))
        hapus = tk.Label(self, image = hapusImg)
        hapus.image = hapusImg

        f2Btn2 = tk.Button(self, image=hapusImg, padx=10, pady=10, fg='black',
                        font=("Helvetica 10 bold"), borderwidth=0, bg='#494949',command=self.delRow)

        tambahImg  = ImageTk.PhotoImage((Image.open('assets/tambah.png')).resize((100,40)))
        tambah = tk.Label(self, image = tambahImg)
        tambah.image = tambahImg

        f2Btn3 = tk.Button(self, image=tambahImg, padx=10, pady=10, fg='black',
                        font=("Helvetica 10 bold"), borderwidth='0', bg='#494949',command=self.addRow)

        nextImg  = ImageTk.PhotoImage((Image.open('assets/berikutnya.png')).resize((250,80)))
        next = tk.Label(self, image = nextImg)
        next.image = nextImg

        self.f2Btn4 = tk.Button(self, image=nextImg, padx=10, pady=10, fg='black', state=DISABLED,
                        font=("Helvetica 10 bold"), borderwidth='0', bg='#363636',command = lambda : [self.storeValue(), controller.refresh_frame(Frame3)])

        #f2Btn1.grid(row=0, column=0, padx=10, pady=10, ipady=1, ipadx=5)
        backButton.place(relx=0.16, rely=0.2, anchor=CENTER)
        #f2Label1.place(relx=0.37, rely=0.205, anchor=CENTER)
        f2Btn2.place(relx=0.28, rely=0.32, anchor=CENTER)
        f2Btn3.place(relx=0.38, rely=0.32, anchor=CENTER)
        self.f2Btn4.place(relx=0.77, rely=0.81, anchor=CENTER)


class Frame3(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        screenWidth = self.winfo_screenwidth()
        screenHeight = self.winfo_screenheight()

        background_image = ImageTk.PhotoImage((Image.open('assets/frame3.png')).resize((screenWidth, screenHeight)))
        background_label = tk.Label(self, image=background_image)
        background_label.image = background_image
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        logoBackImg = ImageTk.PhotoImage((Image.open('assets/back.png')).resize((80, 80)))
        logoBack = tk.Label(self, image=logoBackImg)
        logoBack.image = logoBackImg
        backButton = tk.Button(self, image=logoBackImg, bg="#585858", borderwidth=0,
                               command=lambda: controller.show_frame(Frame2))

        #f3Label1 = tk.Label(self, text="Silahkan melakukan inisialisasi\n slot parkir seperti contoh berikut", padx=10,
        #                    pady=10,
        #                    font=('Helvetica 30 bold'), bg='#585858', fg='white')
        f3Label2 = tk.Label(self,
                            text="Apabila terdapat salah klik, klik \nkanan mouse untuk undo \n Tekan 'C' untuk ke baris selanjutnya",
                            padx=10,
                            pady=10, font=('Helvetica 20 bold'), bg='#444444', fg='#ff6200')

        uploadImg = ImageTk.PhotoImage((Image.open('assets/upload.png')).resize((250, 80)))
        upload = tk.Label(self, image=uploadImg)
        upload.image = uploadImg
        f3Btn2 = tk.Button(self, image=uploadImg, padx=10, pady=10, fg='black',
                           font=("Helvetica 10 bold"), borderwidth=0, bg='#363636', command=select_image)

        nextImg = ImageTk.PhotoImage((Image.open('assets/berikutnya.png')).resize((250, 80)))
        next = tk.Label(self, image=nextImg)
        next.image = nextImg
        f3Btn3 = tk.Button(self, image=nextImg, padx=10, pady=10, fg='black',
                           font=("Helvetica 10 bold"), borderwidth=0, bg='#363636',
                           command=lambda: controller.refresh_frame(Frame4))

        backButton.place(relx=0.16, rely=0.2, anchor=CENTER)

        #f3Label1.place(relx=0.4, rely=0.205, anchor=CENTER)
        f3Label2.place(relx=0.6, rely=0.5, anchor=CENTER)

        f3Btn2.place(relx=0.28, rely=0.81, anchor=CENTER)
        f3Btn3.place(relx=0.77, rely=0.81, anchor=CENTER)

        anim = MyLabel(self, 'assets/gifz.gif')
        # anim.pack()

        anim.place(relx=0.28, rely=0.5, anchor=CENTER)


class Frame4(tk.Frame):
    def getROISlot(self):
        global ROISlot
        ROISlot = Detection.inisialisasi(self, path, rowValue)
        self.f4Label1['text'] = 'INISIALISASI SELESAI'

    def saveKoordinat(self):
        global namaFile
        arr = np.array(ROISlot, dtype=object)
        namaFile = self.f4Entry1.get()
        save("data/" + str(namaFile) + ".npy", arr)
        # np.save("data/"+str(namaFile)+".npy",arr)
        print('END')

    def clear(self):
        rowLabel = {}
        rowEntry = {}
        row = 0

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        screenWidth = self.winfo_screenwidth()
        screenHeight = self.winfo_screenheight()

        background_image = ImageTk.PhotoImage((Image.open('assets/frame4.png')).resize((screenWidth, screenHeight)))
        background_label = tk.Label(self, image=background_image)
        background_label.image = background_image
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        logoBackImg = ImageTk.PhotoImage((Image.open('assets/back.png')).resize((80, 80)))
        logoBack = tk.Label(self, image=logoBackImg)
        logoBack.image = logoBackImg
        f4Btn1 = tk.Button(self, image=logoBackImg, bg="#585858", borderwidth=0,
                           command=lambda: controller.refresh_frame(Frame3))

        mulaiImg = ImageTk.PhotoImage((Image.open('assets/mulai.png')).resize((250, 80)))
        mulai = tk.Label(self, image=mulaiImg)
        mulai.image = mulaiImg
        f4Btn2 = tk.Button(self, image=mulaiImg, padx=10, pady=10, bg='#444444', borderwidth=0,
                           font=("Helvetica 10 bold"), command=self.getROISlot, )

        selesaiImg = ImageTk.PhotoImage((Image.open('assets/selesai.png')).resize((250, 80)))
        selesai = tk.Label(self, image=selesaiImg)
        selesai.image = selesaiImg
        f4Btn3 = tk.Button(self, image=selesaiImg, padx=10, pady=10, bg='#363636', borderwidth=0,
                           font=("Helvetica 10 bold"),
                           command=lambda: [self.saveKoordinat(), self.clear(), controller.refresh_frame(Frame5)])

        #self.f4Label1 = tk.Label(self, text='Silahkan untuk mulai inisialisasi', padx=10,
        #                         pady=10, font=('Helvetica 25 bold'), fg='white', bg='#555555')
        f4Label2 = tk.Label(self, text="Nama area = ", padx=10,
                            pady=10, font=('Helvetica 20 bold'), bg='#4e4e4e', fg='white')
        self.f4Entry1 = tk.Entry(self, bd=5)

        f4Btn1.place(relx=0.16, rely=0.2, anchor=CENTER)
        #self.f4Label1.place(relx=0.4, rely=0.205, anchor=CENTER)
        f4Label2.place(relx=0.45, rely=0.38, anchor=CENTER)
        f4Btn2.place(relx=0.5, rely=0.5, anchor=CENTER)
        f4Btn3.place(relx=0.77, rely=0.81, anchor=CENTER)
        self.f4Entry1.place(relx=0.57, rely=0.38, anchor=CENTER)


class Frame5(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        screenWidth = self.winfo_screenwidth()
        screenHeight = self.winfo_screenheight()

        background_image = ImageTk.PhotoImage((Image.open('assets/frame5.png')).resize((screenWidth, screenHeight)))
        background_label = tk.Label(self, image=background_image)
        background_label.image = background_image
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        f5Label1 = tk.Label(self, text="Koordinat slot parkir dengan\nnama " + namaFile + "\ntelah berhasil disimpan.",
                            padx=10, pady=10, font=('Helvetica 35 bold'), fg='white', bg='#505050')
        #f5Label2 = tk.Label(self, text="Apakah anda ingin melakukan\ninisialisasi area parkir lainnya?", padx=10,
        #                    pady=10, font=('Helvetica 35 bold'), fg='#ff6200', bg='#424242')

        yesImg = ImageTk.PhotoImage((Image.open('assets/ya.png')).resize((250, 80)))
        yes = tk.Label(self, image=yesImg)
        yes.image = yesImg
        f5Btn1 = tk.Button(self, image=yesImg, bg="#383838", borderwidth=0,
                           command=lambda: controller.refresh_frame(Frame2))

        noImg = ImageTk.PhotoImage((Image.open('assets/tidak.png')).resize((250, 80)))
        no = tk.Label(self, image=noImg)
        no.image = noImg
        f5Btn2 = tk.Button(self, image=noImg, bg="#383838", borderwidth=0,
                           command=lambda: controller.refresh_frame(Frame6))

        """ f5Label1.grid(row=0,column=2,columnspan=4,padx=15,pady=15)
        f5Label2.grid(row=1,column=2,columnspan=4,padx=15,pady=15)
        f5Btn1.grid(row=2,column=6,padx=15,pady=15)
        f5Btn2.grid(row=2,column=7,padx=15,pady=15) """
        f5Label1.place(relx=0.5, rely=0.3, anchor=CENTER)
        #f5Label2.place(relx=0.5, rely=0.5, anchor=CENTER)
        f5Btn1.place(relx=0.35, rely=0.75, anchor=CENTER)
        f5Btn2.place(relx=0.65, rely=0.75, anchor=CENTER)


class Frame6(tk.Frame):
    def __init__(self, parent, controller):
        curdir = os.getcwd() + "\data"
        print(curdir)
        print(os.listdir(curdir))
        coordinateDict = os.listdir(curdir)
        NewCoordineteDict = [i[:-4] for i in coordinateDict]

        print(NewCoordineteDict)

        # os.chdir(curdir+)

        tk.Frame.__init__(self, parent)

        screenWidth = self.winfo_screenwidth()
        screenHeight = self.winfo_screenheight()

        background_image = ImageTk.PhotoImage((Image.open('assets/frame6.png')).resize((screenWidth, screenHeight)))
        background_label = tk.Label(self, image=background_image)
        background_label.image = background_image
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        logoBackImg = ImageTk.PhotoImage((Image.open('assets/back.png')).resize((80, 80)))
        logoBack = tk.Label(self, image=logoBackImg)
        logoBack.image = logoBackImg
        f4Btn1 = tk.Button(self, image=logoBackImg, bg="#585858", borderwidth=0,
                           command=lambda: controller.refresh_frame(Frame1))



        value_inside = tk.StringVar(self)
        value_inside.set("Select an Option")

        f6DropDown = tk.OptionMenu(self, value_inside, *NewCoordineteDict)


        def get_coordinate():
            global coordinatePath

            coordinate = value_inside.get()
            coordinatePath = curdir + "\\" + coordinate + ".npy"
            print("Cek:" + coordinatePath)

            return None


        uploadImg = ImageTk.PhotoImage((Image.open('assets/upload.png')).resize((250, 80)))
        upload = tk.Label(self, image=uploadImg)
        upload.image = uploadImg
        f6Btn2 = tk.Button(self, image=uploadImg, padx=10, pady=10, fg='black',
                           font=("Helvetica 10 bold"), borderwidth=0, bg='#363636', command=select_image)

        nextImg  = ImageTk.PhotoImage((Image.open('assets/berikutnya.png')).resize((250,80)))
        next = tk.Label(self, image = nextImg)
        next.image = nextImg
        f6Btn3 = tk.Button(self, image=nextImg, padx=10, pady=10, fg='black',
                        font=("Helvetica 10 bold"), borderwidth='0', bg='#363636',command = lambda : [get_coordinate(), controller.refresh_frame(Frame7)])




        f4Btn1.place(relx=0.16, rely=0.2, anchor=CENTER)

        f6DropDown.place(relx=0.28, rely=0.38, anchor=CENTER)

        f6Btn2.place(relx=0.55, rely=0.81, anchor=CENTER)
        f6Btn3.place(relx=0.77, rely=0.81, anchor=CENTER)




class Frame7(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        screenWidth = self.winfo_screenwidth()
        screenHeight = self.winfo_screenheight()

        background_image = ImageTk.PhotoImage((Image.open('assets/frame7.png')).resize((screenWidth, screenHeight)))
        background_label = tk.Label(self, image=background_image)
        background_label.image = background_image
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        global inputText, outputText
        global slot1Text, slot2Text, slot3Text, slot1Result, slot2Result, slot3Result
        global panelA, panelB, plottedImage, image

        logoHomeImg = ImageTk.PhotoImage((Image.open('assets/home.png')).resize((100, 80)))
        logoHome = tk.Label(self, image=logoHomeImg)
        logoHome.image = logoHomeImg
        homeButton = tk.Button(self, image=logoHomeImg, borderwidth=0, command=lambda: [controller.show_frame(Frame1)])
        homeButton.configure(bg='#353535')
        homeButton.place(relx=0.74, rely=0.8, anchor=CENTER)


        #btn = tk.Button(self, text="Home", command=lambda: [controller.show_frame(Frame1)])
        #btn.grid(row=3, column=7, padx='10', pady='10')



        logoExitImg = ImageTk.PhotoImage((Image.open('assets/exit.png')).resize((80, 80)))
        logoExit = tk.Label(self, image=logoExitImg)
        logoExit.image = logoExitImg
        exitButton = tk.Button(self, image=logoExitImg, borderwidth=0, command=lambda: [sys.exit()])
        exitButton.configure(bg='#353535')

        exitButton.place(relx=0.83, rely=0.8, anchor=CENTER)
        #btn2 = Button(self, text="Exit", command=lambda: [sys.exit()])
        #btn2.grid(row=3, column=8, padx='10', pady='10')

        self.load()

    def load(self):
        image = cv2.imread(path)

        index, box = Detection.car_detection(self, image)
        outImg, slot2Value, slot3Value = Detection.determine_occupancy(self, indexes=index, box=box, path=path,
                                                                       coordinatePath=coordinatePath)

        screen_width = self.winfo_screenwidth()
        img_width = int((35 / 100) * screen_width)
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


        # the first panel will store our original image
        panelA = tk.Label(self, image=image, bg='#ff6200')
        panelA.image = image
        # panelA.pack(side="left", padx=10, pady=10)
        panelA.place(relx=0.32, rely=0.45, anchor=CENTER)

        #panelA.grid(row=1, column=0, columnspan=6, padx='10', pady='10')

        # while the second panel will store the edge map
        panelB = tk.Label(self, image=plottedImage, bg='#ff6200')
        panelB.image = plottedImage
        # panelB.pack(side="right", padx=10, pady=10)

        panelB.place(relx=0.68, rely=0.45, anchor=CENTER)
        #panelB.grid(row=1, column=6, columnspan=6, padx='10', pady='10')

        # text untuk keterangan slot (total, occupied, dan vacant)
        # Total slot
        slot1Text = tk.Label(self, text='Total lahan parkir      ', font=('Arial', 14), pady=5, fg='white',bg='#383838')
        slot1Text.place(relx=0.2, rely=0.74, anchor=CENTER)
        #slot1Text.grid(row=2, column=1)
        # Occupied slot
        slot2Text = tk.Label(self, text='Lahan parkir terisi    ', font=('Arial', 14), pady=5, fg='white',bg='#353535')
        slot2Text.place(relx=0.2, rely=0.79, anchor=CENTER)
        #slot2Text.grid(row=3, column=1)
        # Vacant slot
        slot3Text = tk.Label(self, text='Lahan parkir kosong', font=('Arial', 14), pady=5, fg='white',bg='#323232')
        slot3Text.place(relx=0.2, rely=0.84, anchor=CENTER)
        #slot3Text.grid(row=4, column=1)

        # text untuk hasil slot (total, occupied, dan vacant)
        # Total slot
        slot1Result = tk.Label(self, text=str(slot2Value + slot3Value), font=('Arial', 14), pady=10, fg='#ff6200',bg='#383838')
        slot1Result.place(relx=0.3, rely=0.74, anchor=CENTER)
        #slot1Result.grid(row=2, column=3)
        # Occupied slot
        slot2Result = tk.Label(self, text=str(slot2Value), font=('Arial', 14), pady=10, fg='#ff6200',bg='#353535')
        slot2Result.place(relx=0.3, rely=0.79, anchor=CENTER)
        #slot2Result.grid(row=3, column=3)
        # Vacant slot
        slot3Result = tk.Label(self, text=str(slot3Value), font=('Arial', 14), pady=10, fg='#ff6200',bg='#323232')
        slot3Result.place(relx=0.3, rely=0.84, anchor=CENTER)
        #slot3Result.grid(row=4, column=3)



# run the GUI
app = tkinterApp()
app.attributes('-fullscreen',True)
app.title('Smart Parking System V1.0')
#app.wm_attributes('-transparentcolor', app['bg'])
app.mainloop()