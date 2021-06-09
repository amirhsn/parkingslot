import cv2
import numpy as np
import os
from tkinter import *
from PIL import Image


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