#Import modul
from PIL import Image                                   
import cv2                                              
import numpy as np                                      
import matplotlib.pyplot as plt 

#Load images
image = cv2.imread("data/tes.jpg")
image = cv2.resize(image, (image.shape[1],image.shape[0]), interpolation = cv2.INTER_AREA)
plottedImage = image.copy()
#cv2.imshow("Image",plottedImage)
#cv2.waitKey(0)
#cv2.destroyAllWindows()

#Load koodinat npy
ROI_slot = np.load('data/dua.npy',allow_pickle=True)

#Plotting
for row in range(len(ROI_slot)):
    for slots in range(len(ROI_slot[row])):
        for titik in range (len(ROI_slot[row][slots])):
            if ROI_slot[row][slots][titik][0] == None:
                pass
            else:
                x1 = ROI_slot[row][slots][titik][0]
                y1 = ROI_slot[row][slots][titik][1]
                if titik==3:
                    x2 = ROI_slot[row][slots][0][0]
                    y2 = ROI_slot[row][slots][0][1]
                else:
                    x2 = ROI_slot[row][slots][titik+1][0]
                    y2 = ROI_slot[row][slots][titik+1][1]
                cv2.line(plottedImage,(x1,y1),(x2,y2),(0,0,255),1)

cv2.imshow("Image",plottedImage)
cv2.waitKey(0)
cv2.destroyAllWindows()