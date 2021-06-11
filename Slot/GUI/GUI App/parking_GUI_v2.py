import cv2
import tkinter as tk
import numpy as np
import math
import os
from os import listdir
from os.path import isfile, join
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from PIL import Image
from PIL import ImageTk
from shapely.geometry import Polygon
from numpy import save
from PIL.ImageTk import PhotoImage


#root.title('Parking Slot App')
#initialize each frame
#frame1 = tk.Frame(root)
#frame2 = tk.Frame(root)
#frame3 = tk.Frame(root)
#frame4 = tk.Frame(root)
#frame5 = tk.Frame(root)
#frame6 = tk.Frame(root)
#frame7 = tk.Frame(root)

row = 0
rowLabel = dict()
rowEntry = dict()
panelA = None
panelB = None
rowValue = []
path = ''
ROISlot = []


def select_image():
    global path

    path = filedialog.askopenfilename()
    print(path)


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

def car_detection(image):
    box = []
    classes = []
    indexes = 0

    # Load Yolo
    net = cv2.dnn.readNet("yolov4-obj_best.weights", "yolov4-obj.cfg")
    # net = cv2.dnn.readNet("20_yolov3.weights","20_yolov3.cfg")

    with open("obj.names", "r") as f:
        classes = [line.strip() for line in f.readlines()]
    layer_names = net.getLayerNames()
    output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]

    # Loading image
    height, width, channels = image.shape

    # Detecting objects
    blob = cv2.dnn.blobFromImage(image, 0.00392, (608, 608), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(output_layers)

    # Showing information on the screen
    class_ids = []
    confidences = []
    boxes = []
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.1:
                if class_id == 1:
                    # Object detected
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)

                    # Rectangle coordinates
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)

                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)

    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.1, 0.4)

    font = cv2.FONT_HERSHEY_PLAIN
    color_blue = (255, 0, 0)
    color_red = (0, 0, 255)
    # print(indexes)
    for i in range(len(boxes)):
        if i in indexes:
            x, y, w, h = boxes[i]
            box.append(boxes[i])
            label = str(classes[class_ids[i]])

    #            cv2.rectangle(image, (x, y), (x + w, y + h), color_blue, 2)
    #            cv2.putText(image, label, (x, y + 30), font, 2, color_blue, 2)
    #            cv2.putText(image, str("{:.2f}".format(confidences[i])), (x, y + 50), font, 2, color_red, 2)

    #    cv2.imshow("output1",image)
    #    cv2.waitKey(0)
    #    cv2.destroyAllWindows()

    return indexes, box


# DRAW LINE
distancez = []


def euclideanDistance(coordinate1, coordinate2):
    return pow(pow(coordinate1[0] - coordinate2[0], 2) + pow(coordinate1[1] - coordinate2[1], 2), .5)


def determine_occupancy(indexes, box):
    global slot2Value, slot3Value
    slot2Value = 0
    slot3Value = 0
    boxess = []
    ROI_car = []
    ED = []
    perc_ED = []
    temp = []
    IoU = []
    Status = []
    diagonal_slot = []
    centroid_slot_x = []
    centroid_slot_y = []
    area_slot = []

    carX = 0
    carY = 0
    allCentroidCar = []
    ED = []
    perc_ED = []
    Status = []
    min_ed_car = []
    car_id = []
    count = 0
    idx_and_car = []
    idx_car_list = []
    IoU = []
    slotImage = []
    carImage = []
    iou = []
    car_idx = []

    # Load koodinat npy
    ROI_slot = np.load('data/CNR_camera8.npy', allow_pickle=True)
    for i in range(len(indexes)):
        boxess.append([])
        boxess[i].append(box[i][0])
        boxess[i].append(box[i][1])
        boxess[i].append(box[i][2] + box[i][0])
        boxess[i].append(box[i][3] + box[i][1])

    for i in range(len(indexes)):
        ROI_car.append([(boxess[i][0], boxess[i][3]), (boxess[i][0], boxess[i][1]), (boxess[i][2], boxess[i][1]),
                        (boxess[i][2], boxess[i][3])])

    # inisialisasi array
    for i in range(len(ROI_slot)):
        new = []
        new1 = []
        new2 = []
        new3 = [0, 0]
        for j in (ROI_slot[i]):
            new.append(0)
            new1.append(0)
            new2.append(0)
        diagonal_slot.append(new)
        centroid_slot_x.append(new1)
        centroid_slot_y.append(new2)

    for i in range(len(ROI_slot)):
        new = []
        for j in (ROI_slot[i]):
            new.append(0)
        area_slot.append(new)

    for row in range(len(ROI_slot)):
        for slots in range(len(ROI_slot[row])):
            x1 = ROI_slot[row][slots][0][0]
            y1 = ROI_slot[row][slots][0][1]
            x2 = ROI_slot[row][slots][1][0]
            y2 = ROI_slot[row][slots][1][1]
            x3 = ROI_slot[row][slots][2][0]
            y3 = ROI_slot[row][slots][2][1]
            x4 = ROI_slot[row][slots][3][0]
            y4 = ROI_slot[row][slots][3][1]

            # menghitung centroid slot
            centroid_slot_x[row][slots] = (x3 + x1) / 2
            centroid_slot_y[row][slots] = (y3 + y1) / 2

            d1 = math.sqrt(((y3 - y1) ** 2) + ((x3 - x1) ** 2))
            d2 = math.sqrt(((y4 - y2) ** 2) + ((x4 - x2) ** 2))
            if d1 < d2:
                diagonal_slot[row][slots] = d1
            else:
                diagonal_slot[row][slots] = d2

            area_slot[row][slots] = (
                abs(((x1 * y2 - y1 * x2) + (x2 * y3 - y2 * x3) + (x3 * y4 - y3 * x4) + (x4 * y1 - y4 * x1)) / 2))

    # plotting slot parkir
    plottedImage = image.copy()
    rows, cols, channels = plottedImage.shape
    for i in range(len(ROI_slot)):
        new = []
        new1 = []
        new2 = []
        for j in (ROI_slot[i]):
            new.append(0)
            new1.append(0)
            new2.append(0)
        ED.append(new)
        perc_ED.append(new)
        Status.append(new1)
        IoU.append(new2)

    # gambar titik centroid di mobil
    for car in range(len(ROI_car)):
        x1 = ROI_car[car][0][0]
        y1 = ROI_car[car][0][1]
        x3 = ROI_car[car][2][0]
        y3 = ROI_car[car][2][1]
        centroid_car_x = (x1 + x3) / 2
        centroid_car_y = (y1 + y3) / 2
        allCentroidCar.append((int(centroid_car_x), int(centroid_car_y)))
        mod = cv2.circle(plottedImage, (int(centroid_car_x), int(centroid_car_y)), 4, (0, 0, 255), -1)

    intersect = []
    count = 0

    for row in range(len(ROI_slot)):
        slotImage.append([])
        carImage.append([])
        iou.append([])
        for slots in range(len(ROI_slot[row])):
            slotImage[row].append([])
            carImage[row].append([])
            iou[row].append([])
            slotImage[row][slots] = np.zeros_like(image)
            carImage[row][slots] = np.zeros_like(image)

            centroid_slot_xx = centroid_slot_x[row][slots]
            centroid_slot_yy = centroid_slot_y[row][slots]
            # titik di slot
            mod = cv2.circle(plottedImage, (int(centroid_slot_xx), int(centroid_slot_yy)), 4, (0, 0, 255), -1)
            temp = []
            temp2 = []
            for car in range(len(ROI_car)):
                x1 = ROI_car[car][0][0]
                y1 = ROI_car[car][0][1]
                x3 = ROI_car[car][2][0]
                y3 = ROI_car[car][2][1]

                centroid_car_x = (x1 + x3) / 2
                centroid_car_y = (y1 + y3) / 2

                temp.append(
                    math.sqrt(((centroid_slot_yy - centroid_car_y) ** 2) + ((centroid_slot_xx - centroid_car_x) ** 2)))
                temp2.append(car)
                p = Polygon(ROI_slot[row][slots])
                q = Polygon(ROI_car[car])
                intersect.append(q.intersection(p).area)

            min_ed = min(temp)

            idx = temp.index(min(temp))
            idx_car = temp2[idx]
            idx_car_list.append(idx_car)
            min_ed_car.append([idx_car, row, slots, min_ed])

            roi1 = np.array(ROI_slot[row][slots])
            roi2 = np.array(ROI_car[idx_car])
            cv2.fillPoly(slotImage[row][slots], pts=[roi1], color=(0, 0, 255))
            cv2.fillPoly(carImage[row][slots], pts=[roi2], color=(0, 0, 255))
            iou[row][slots] = cv2.bitwise_and(slotImage[row][slots], carImage[row][slots])
            iouu = np.array(iou[row][slots])
            # print(iouu)
            dst = cv2.add(plottedImage, iouu)
            plottedImage[0:rows, 0:cols] = dst

            ED[row][slots] = min(temp)
            perc_ED[row][slots] = (ED[row][slots] / diagonal_slot[row][slots]) * 100

            max_intrsct = max(intersect)
            IoU[row][slots] = ((max_intrsct / area_slot[row][slots]) * 100)

            if perc_ED[row][slots] < 75:
                if IoU[row][slots] == 0:
                    Status[row][slots] = 'VACANT'
                elif IoU[row][slots] > 0:
                    Status[row][slots] = 'OCCUPIED'
            else:
                Status[row][slots] = 'VACANT'

    x = [min_ed_car[i][0] for i in range(len(min_ed_car))]
    h = max(idx_car_list)

    for count in range(h + 1):
        tempp = []
        slott = []
        for i in range(len(x)):
            if (x[i] in x[:i]) or (x[i] in x[i + 1:]):
                if x[i] == count:
                    tempp.append(min_ed_car[i][3])
                    slott.append([min_ed_car[i][1], min_ed_car[i][2]])
        if not tempp:
            minn = 99999
        else:
            minn = min(tempp)
            indx = tempp.index(min(tempp))
            for i in range(len(slott)):
                if (i == indx):
                    ED[slott[i][0]][slott[i][1]] = minn
                    perc_ED[slott[i][0]][slott[i][1]] = (ED[slott[i][0]][slott[i][1]] / diagonal_slot[slott[i][0]][
                        slott[i][1]]) * 100
                    if perc_ED[slott[i][0]][slott[i][1]] < 75:
                        Status[slott[i][0]][slott[i][1]] = 'OCCUPIED'
                    else:
                        Status[slott[i][0]][slott[i][1]] = 'VACANT'
                else:
                    Status[slott[i][0]][slott[i][1]] = 'VACANT'

    for row in range(len(ROI_slot)):
        for slots in range(len(ROI_slot[row])):
            if Status[row][slots] == 'OCCUPIED':
                slot2Value += 1
            else:
                slot3Value += 1

    fontScale = 0.8

    for row in range(len(ROI_slot)):
        for slots in range(len(ROI_slot[row])):
            # draw ROI_slot
            mod = cv2.polylines(plottedImage, np.int32([ROI_slot[row][slots]]), True, (255, 0, 0), thickness=2)
            # draw Status_slot
            mod = cv2.putText(plottedImage, Status[row][slots],
                              (int(centroid_slot_x[row][slots]) - 10, int(centroid_slot_y[row][slots])),
                              cv2.FONT_HERSHEY_SIMPLEX, 0.3, (255, 255, 0), 1, cv2.LINE_AA)
            # Text slot
            # PENTING extY GANTI KE '0' UNTUK CAMERA 8 DAN '15' UNTUK CAMERA 1. BIAR TIDAK TUMPANG TINDIH
            extY = 0
            minROISlot = min(ROI_slot[row][slots])
            org = (minROISlot[0], minROISlot[1] + extY)
            slotId = "(" + str(row) + "-" + str(slots) + ")"
            font = cv2.FONT_HERSHEY_PLAIN
            cv2.putText(plottedImage, slotId, org, font, fontScale, (255, 255, 255), 1)

    for row in range(len(ROI_slot)):
        for slots in range(len(ROI_slot[row])):
            distancez = []
            if Status[row][slots] == 'VACANT':
                continue
            else:
                centSlotX = int(centroid_slot_x[row][slots])
                centSlotY = int(centroid_slot_y[row][slots])
                for i in allCentroidCar:
                    distancez.append(euclideanDistance((centSlotX, centSlotY), (i[0], i[1])))
                minDistancezIndex = distancez.index(min(distancez))
                centCarX = allCentroidCar[minDistancezIndex][0]
                centCarY = allCentroidCar[minDistancezIndex][1]
                mod = cv2.line(plottedImage, (centSlotX, centSlotY), (centCarX, centCarY), (0, 255, 255), 2)

    return plottedImage



def inisialisasi():
    image = cv2.imread("data/CNR/samples/cam8.jpg")
    image = cv2.resize(image, (image.shape[1], image.shape[0]), interpolation=cv2.INTER_AREA)
    state = 0
    sum_rows = 0
    sum_slots = []
    font = cv2.FONT_HERSHEY_PLAIN
    ROI_slot = []
    imges = image.copy()
    original_clone = image.copy()
    clone = Image.fromarray(original_clone)
    jumlahSlot = [2, 3, 4]

    def coordinate(event, x, y, flags, param):
        global point, click, keyPoint, tAwal, tAkhir, indexClick, rowIndicator, cache, image, tAwalTemp, tAkhirTemp

        if event == cv2.EVENT_LBUTTONDOWN:
            cache = np.copy(image)

            tAwalTemp = tAwal
            tAkhirTemp = tAkhir

            rowIndicator = rowIndicator + 1
            point = (x, y)
            keyPoint.append(point)
            print(keyPoint)
            click = click + 1
            if click == 1:
                tAkhir = tAwal + 1
                cv2.line(image, keyPoint[tAwal], keyPoint[tAkhir], (0, 0, 255), 2)
            elif click == 2:
                tAwal = tAkhir
                tAkhir = tAkhir + 1
                cv2.line(image, keyPoint[tAwal], keyPoint[tAkhir], (0, 0, 255), 2)
            elif click == 3:
                tAwal = tAkhir
                tAkhir = tAkhir + 1
                cv2.line(image, keyPoint[tAwal], keyPoint[tAkhir], (0, 0, 255), 2)
                cv2.line(image, keyPoint[tAwal - 2], keyPoint[tAkhir], (0, 0, 255), 2)
                click = 1
            # Deteksi jika sudah memenuhi jumlah slot, maka move ke row/shaf berikutnya
            # PAKAI ARITMATIKA a+(n-1)*b menjadi 2+2.n
            if rowIndicator == (2 + 2 * (jumlahSlot[row])):
                print(rowIndicator)
                print('DONE')

        if event == cv2.EVENT_RBUTTONDOWN:
            # HOW TO DELETE?
            image = np.copy(cache)
            if click == 1:
                click = 3
            click = click - 1
            tAwal = tAwalTemp
            tAkhir = tAkhirTemp
            del keyPoint[-1]

    for row in range(len(jumlahSlot)):
        # undoImage = image
        # undoCheck = False
        rowIndicator = 0
        point = []
        keyPoint = []
        click = -1
        tAkhir = 0
        tAwal = 0

        tAkhirTemp = 0
        tAwalTemp = 0

#        global image
#        global cache

        image = original_clone.copy()
        cache = np.copy(image)

        cv2.namedWindow('image')
        cv2.setMouseCallback('image', coordinate)

        while True:
            cv2.imshow('image', image)
            if cv2.waitKey(1) == ord('c'):
                break

        cv2.destroyAllWindows()

        ROI_slot.append([])
        for i in range(jumlahSlot[row]):
            ROI_slot[row].append([])
            ROI_slot[row][i].append([keyPoint[0 + i + i][0], keyPoint[0 + i + i][1]])
            ROI_slot[row][i].append([keyPoint[1 + i + i][0], keyPoint[1 + i + i][1]])
            ROI_slot[row][i].append([keyPoint[2 + i + i][0], keyPoint[2 + i + i][1]])
            ROI_slot[row][i].append([keyPoint[3 + i + i][0], keyPoint[3 + i + i][1]])

        #Export ke npy
        savedir = os.getcwd()+"\data"
        arr = np.array(ROI_slot)
        save(savedir,arr)



#def im_location():
#    img_location = select_image()
#    return img_location

class tkinterApp(tk.Tk):

    # __init__ function for class tkinterApp
    def __init__(self, *args, **kwargs):
        global container
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
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        f2Btn1 = tk.Button(self, text='Back', padx=10, pady=10, fg='black', height=1, width=5,
                        font=("Helvetica 10 bold"))
        f2Label1 = tk.Label(self, text="Masukkan jumlah slot parkir pada setiap barisnya", padx=10, pady=10,
                         font=('Helvetica 12 bold'))
        f2Label2 = Label(self, text="NU IE ACAN", padx=10, pady=10, font=('Helvetica 12 bold'), height=10)

        f2Btn2 = tk.Button(self, text='Hapus baris', padx=10, pady=10, fg='black', height=1, width=10,
                        font=("Helvetica 10 bold"), command=delRow)
        f2Btn3 = tk.Button(self, text='Tambah baris', padx=10, pady=10, fg='black', height=1, width=10,
                        font=("Helvetica 10 bold"), command=addRow)

        f2Btn4 = tk.Button(self, text='Berikutnya', padx=10, pady=10, fg='black', height=1, width=15,
                        font=("Helvetica 10 bold"), command = lambda : controller.show_frame(Frame4))
        f2Label2 = tk.Label(self, text="NU IE ACAN", padx=10, pady=10, font=('Helvetica 12 bold'), height=10)

        f2Btn1.grid(row=0, column=0, padx=10, pady=10, ipady=1, ipadx=5)
        f2Label1.grid(row=1, column=0, columnspan=4, padx=6, pady=6)
        f2Label2.grid(row=3, column=0)
        f2Btn2.grid(row=2, column=0, padx=8, pady=8,ipady=1, ipadx=10)
        f2Btn3.grid(row=2, column=1, padx=8, pady=8, ipady=1, ipadx=10)
        f2Btn4.grid(row=4, column=1, padx=8, pady=8, ipady=1, ipadx=15)


class Frame3(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        f3Btn1 = tk.Button(self, text='Back', padx=10, pady=10, fg='black', height=1, width=5,
                        font=("Helvetica 10 bold"))
        f3Label1 = tk.Label(self, text="Silahkan melakukan inisialisasi\nslot seperti contoh berikut", padx=10, pady=10,
                         font=('Helvetica 12 bold'))
        f3Label2 = tk.Label(self, text="Apabila terdapat salah klik, tekan\n'Z' untuk kembali ke awal baris", padx=10,
                         pady=10, font=('Helvetica 12 bold'))


        f3Btn2 = tk.Button(self, text='Upload gambar', padx=10, pady=10, fg='black', height=1, width=15,
                        font=("Helvetica 10 bold"))

        f3Btn1.grid(row=0, column=0, padx=10, pady=10, ipady=1, ipadx=5)

        f3Btn1.grid(row=0, column=0, padx=10, pady=10)

        f3Label1.grid(row=1, column=0, columnspan=2, padx=6, pady=6)
        f3Label2.grid(row=3, column=0, columnspan=2, padx=6, pady=6)

        anim = MyLabel(self, 'gifz.gif')
        #anim.pack()

        anim.grid(row=1, column=2, padx=10, pady=10)


        f3Btn2.grid(row=0, column=0, padx=10, pady=10, ipady=1, ipadx=5)


class Frame4(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        f1Btn4 = tk.Button(self, text='Berikutnya', padx=10, pady=10, fg='black', height=1, width=15,
                        font=("Helvetica 10 bold"), command = lambda : controller.show_frame(Frame5))

        f1Btn4.grid(row=4, column=1, padx=8, pady=8, ipady=1, ipadx=15)

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

        f6DropDown = tk.OptionMenu(self, value_inside, *coordinateDict)
        #f6DropDown.pack()



        def get_coordinate():
            global coordinate, path
            coordinate = value_inside.get()
            path = curdir + "\\" + coordinate

            return None

        submit_button = tk.Button(self, text='Submit', command=lambda :[get_coordinate(), controller.show_frame(Frame7)])


        f6Btn2 = tk.Button(self, text='Upload gambar', padx=10, pady=10, fg='black', height=1, width=15,
                            font=("Helvetica 10 bold"),command = select_image)


        f6Btn3 = tk.Button(self, text='Berikutnya', padx=25, pady=10, fg='black', height=1, width=15,
                            font=("Helvetica 10 bold"), command = lambda : controller.show_frame(Frame1))

        f6Btn1.grid(row=0, column=0, padx=10, pady=10)
        f6Label1.grid(row=1, column=0, columnspan=4, padx=10, pady=15)
        f6DropDown.grid(row=2, column=0, rowspan=2, padx=10, pady=15)
        f6Btn2.grid(row=5, column=1, pady=20, padx=10)
        f6Btn3.grid(row=5, column=2, pady=20, padx=25)
        submit_button.grid(row=5, column=3, pady=20, padx=25)


class Frame7(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        global inputText, outputText
        global slot1Text, slot2Text, slot3Text, slot1Result, slot2Result, slot3Result
        global panelA, panelB, edged, image

        panelA = None
        panelB = None


        image = cv2.imread(path)
        #image = cv2.imread("C:/Users/ujang/Desktop/sampel gambar/SUNNY/camera8.jpg")

        index, box = car_detection(image)
        outImg = determine_occupancy(indexes=index, box=box)

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
            slot1Result = tk.Label(self,text='= ' + str(slot2Value + slot3Value), font=('Arial', 14), pady=10, fg='red')
            slot1Result.grid(row=2, column=3)
            # Occupied slot
            slot2Result = tk.Label(self,text='= ' + str(slot2Value), font=('Arial', 14), pady=10, fg='red')
            slot2Result.grid(row=3, column=3)
            # Vacant slot
            slot3Result = tk.Label(self,text='= ' + str(slot3Value), font=('Arial', 14), pady=10, fg='red')
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
            slot1Result = tk.Label(self,text='= ' + str(slot2Value + slot3Value), font=('Arial', 14), pady=10, fg='red')
            slot1Result.grid(row=2, column=3)
            # Occupied slot
            slot2Result = tk.Label(self,text='= ' + str(slot2Value), font=('Arial', 14), pady=10, fg='red')
            slot2Result.grid(row=3, column=3)
            # Vacant slot
            slot3Result = tk.Label(self,text='= ' + str(slot3Value), font=('Arial', 14), pady=10, fg='red')
            slot3Result.grid(row=4, column=3)


            btn = tk.Button(self, text="Pilih gambar input", command=select_image)
            btn.grid(row=3, column=7, padx='10', pady='10')
            btn.pack(side="bottom", fill="both", expand="yes", padx="10", pady="10")


# kick off the GUI



app = tkinterApp()
app.mainloop()


