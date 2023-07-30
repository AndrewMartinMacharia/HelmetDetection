import cv2
import pandas as pd
import argparse

# Load the xml file that will be used for getting color names based on their RGB numbers
colors = cv2.CascadeClassifier('RGBcolors.xml')

#Variables for mouse clicking
clicked = False
r = g = b = xpos = ypos = 0

#Creates the argument parser so that the user can input which image to use for testing
argumentParser = argparse.ArgumentParser()
argumentParser.add_argument('-i', '--image', required=True, help="Image Path")
args = vars(argumentParser.parse_args())
imgPath = args['image']

#Reads the image with opencv
img = cv2.imread(imgPath)

# Detecting helmets
helmet = colors.detectMultiScale(image = img, scaleFactor = 1.1, minNeighbors = 5)

#Uses pandas to read the colors csv file.
#Then gives the following names toeach column
index=["color","colorName","hex","R","G","B"]
colorsCSV = pd.read_csv('colors.csv', names=index, header=None)

#This function gets the closest color by calculating the minimum distance
#from all the colors
def getColorName(R,G,B):
    minimum = 10000
    for i in range(len(colorsCSV)):
        d = abs(R- int(colorsCSV.loc[i,"R"])) + abs(G- int(colorsCSV.loc[i,"G"]))+ abs(B- int(colorsCSV.loc[i,"B"]))
        if(d<=minimum):
            minimum = d
            cname = colorsCSV.loc[i,"color_name"]
    return cname

#function to get x,y coordinates of mouse double click
def mouseClick(event, x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        global b,g,r,xpos,ypos, clicked
        clicked = True
        xpos = x
        ypos = y
        b,g,r = img[y,x]
        b = int(b)
        g = int(g)
        r = int(r)
       
cv2.namedWindow('Helmet Color Detector')
cv2.setMouseCallback('Helmet Color Detector',mouseClick)

while(1):

    cv2.imshow("Helmet Color Detector",img) 
    
    for (x, y, w, h) in helmet:
        cv2.rectangle(img, (x, y), (x+w, y+(-1*h)), (150, 0, 0), 2)
        text3 = "Kindly click on a helmet"
        cv2.rectangle(img,(0,235), (245,270), (0,0,0), -1)
        cv2.putText(img, text3,(0,245),5,0.7,(255,255,255),1)
    
        text = "Appropriate helmet color"
        text2 = "Inappropriate helmet color"
        
        #If clicked, and the area clicked is a dark color, it will be an inappropriate color.
        #Otherwise, it will be an appropriate color
        if (clicked):
            if(r+g+b<=255):
                cv2.putText(img, text2,(0,265),5,0.7,(0,0,255),1)
            else:
                cv2.putText(img, text,(0,265),5,0.7,(0,255,0),1)

    #Exits the loop by pressing Esc  
    if cv2.waitKey(20) & 0xFF ==27:
        break
    
cv2.destroyAllWindows()
