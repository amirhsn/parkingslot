import cv2
import numpy as np
import math
from numpy import save
from tkinter import *
from PIL import Image
from shapely.geometry import Polygon


class Detection:
    global slot2Value, slot3Value

    def __init__(self):
        return None
    
    def car_detection(self,image):
        box = []
        classes = []
        indexes = 0

        # Load Yolo
        net = cv2.dnn.readNet("assets/yolov4-obj_best.weights", "assets/yolov4-obj.cfg")
        # net = cv2.dnn.readNet("20_yolov3.weights","20_yolov3.cfg")

        with open("assets/obj.names", "r") as f:
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


    def determine_occupancy(self,indexes, box, path, coordinatePath):

        def euclideanDistance(coordinate1, coordinate2):
            return pow(pow(coordinate1[0] - coordinate2[0], 2) + pow(coordinate1[1] - coordinate2[1], 2), .5)

        image = cv2.imread(path)
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
        ROI_slot = np.load(coordinatePath, allow_pickle=True)
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


                cv2.fillPoly(slotImage[row][slots], pts=np.int32([roi1]), color=(0, 0, 255))

                cv2.fillPoly(carImage[row][slots], pts=np.int32([roi2]), color=(0, 0, 255))



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
            hitung = 0
            for slots in range(len(ROI_slot[row])):
                # draw ROI_slot
                mod = cv2.polylines(plottedImage, np.int32([ROI_slot[row][slots]]), True, (255, 0, 0), thickness=2)
                # draw Status_slot
                mod = cv2.putText(plottedImage, Status[row][slots],
                                (int(centroid_slot_x[row][slots]) - 10, int(centroid_slot_y[row][slots])),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.3, (255, 255, 0), 1, cv2.LINE_AA)



                if hitung %2 == 0:
                    org = (ROI_slot[row][slots][0][0], ROI_slot[row][slots][0][1])
                else:
                    org = (ROI_slot[row][slots][1][0], ROI_slot[row][slots][1][1])

                slotId = "(" + str(row) + "-" + str(slots) + ")"
                font = cv2.FONT_HERSHEY_PLAIN
                cv2.putText(plottedImage, slotId, org, font, fontScale, (255, 255, 255), 1)

                hitung = hitung + 1

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

        return plottedImage, slot2Value, slot3Value




    def inisialisasi(self,pathImage, rowValues):
        global point, click, keyPoint, tAwal, tAkhir, indexClick, rowIndicator, cache, image, tAwalTemp, tAkhirTemp
        image = cv2.imread(pathImage)
        image = cv2.resize(image, (image.shape[1], image.shape[0]), interpolation=cv2.INTER_AREA)
        state = 0
        sum_rows = 0
        sum_slots = []
        font = cv2.FONT_HERSHEY_PLAIN
        ROI_slot = []
        imges = image.copy()
        original_clone = image.copy()
        clone = Image.fromarray(original_clone)
        jumlahSlot = rowValues

        # PAKE INI
        def coordinate(event, x, y, flags, param):
            global point, click, keyPoint, tAwal, tAkhir, indexClick, rowIndicator, cache, image, count
            for i in range(len(jumlahSlot)):
                cv2.putText(image,'Slot baris ke-'+str(i+1)+' = '+str(jumlahSlot[i]),(20,20*(i+1)),font,1,(204,204,0),1,cv2.LINE_AA)
            if event == cv2.EVENT_LBUTTONDOWN:

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

                count = count + 1
                tempp = np.copy(image)
                cache[count] = np.copy(tempp)

            if event == cv2.EVENT_RBUTTONDOWN:
                # HOW TO DELETE?
                image = np.copy(cache[count - 1])
                if click == 1 and tAwal!=0:
                    click = 3
                if tAwal != 0:
                    tAwal = tAwal - 1
                    tAkhir = tAkhir - 1
                if keyPoint:
                    del keyPoint[-1]
                    click = click - 1

                count = count - 1


        # Mulai plot slot

        for row in range(len(jumlahSlot)):
            rowIndicator = 0
            point = []
            keyPoint = []
            click = -1
            tAkhir = 0
            tAwal = 0

            global cache, count

            count = 0

            cache = np.array([np.copy(image) for _ in range(99)])
            tempp = np.copy(image)

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
        
        return ROI_slot