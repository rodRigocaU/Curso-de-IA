import cv2
import numpy as np
import utlis
import pytesseract

########################################################################
webCamFeed = True
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()
custom_config = r'--oem 3 --psm 6'
cap.set(10,110)
heightImg = 640
widthImg  = 680
########################################################################

utlis.initializeTrackbars()
count=0

while True:

#    if webCamFeed:success,img = cap.read()
#    else:
#        img = cv2.imread('03_oswal.png')

    img = cv2.imread('03_oswal.png')
    
    img = cv2.resize(img, (widthImg, heightImg)) # RESIZE IMAGE
    imgBlank = np.zeros((heightImg,widthImg, 3), np.uint8)
    
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
    imgBlur = cv2.GaussianBlur(imgGray, (5, 5), 1)
    thres = utlis.valTrackbars() 

    imgThreshold = cv2.Canny(imgBlur,thres[0],thres[1]) 
    kernel = np.ones((5, 5))
    imgDial = cv2.dilate(imgThreshold, kernel, iterations=2) #elimina blancos
    imgThreshold = cv2.erode(imgDial, kernel, iterations=1)  # engruesa la imagen

    
    imgContours = img.copy() 
    imgBigContour = img.copy() 
    contours, hierarchy = cv2.findContours(imgThreshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(imgContours, contours, -1, (0, 255, 0), 10) 


    
    biggest, maxArea = utlis.biggestContour(contours) 
    
    if biggest.size != 0:
        biggest = utlis.reorder(biggest)
        cv2.drawContours(imgBigContour, biggest, -1, (0, 255, 0), 20)
        imgBigContour = utlis.drawRectangle(imgBigContour,biggest,2)
       
        pts1 = np.float32(biggest)
        pts2 = np.float32([[0, 0],[widthImg, 0], [0, heightImg],[widthImg, heightImg]])
       
        matrix = cv2.getPerspectiveTransform(pts1, pts2)

        imgWarpColored = cv2.warpPerspective(img, matrix, (widthImg, heightImg))

        
        imgWarpColored = imgWarpColored[15:imgWarpColored.shape[0] - 15, 15:imgWarpColored.shape[1] - 15]
        imgWarpColored = cv2.resize(imgWarpColored,(widthImg,heightImg))

        
        imgWarpGray = cv2.cvtColor(imgWarpColored,cv2.COLOR_BGR2GRAY)
        
        print("**************************************" , end="\n") 
        text = pytesseract.image_to_string(imgWarpGray,config=custom_config)
        print('**************************************\n'+text)
        
        #iluminacion variable
        imgAdaptiveThre= cv2.adaptiveThreshold(imgWarpGray, 255, 1, 1, 7, 2)
        imgAdaptiveThre = cv2.bitwise_not(imgAdaptiveThre)
        imgAdaptiveThre=cv2.medianBlur(imgAdaptiveThre,3)
        # Image Array for Display
        imageArray = ([img,imgGray,imgThreshold,imgContours],[imgBigContour,imgWarpColored, imgWarpGray,imgAdaptiveThre])
    else:
        imageArray = ([img,imgGray,imgThreshold,imgContours],[imgBlank, imgBlank, imgBlank, imgBlank])

    #DISPLAY
    lables = [["Original","Gray","Threshold","Contours"],["Contorno","TEST","TEST","Umbral"]]
    stackedImage = utlis.stackImages(imageArray,0.75,lables)
    cv2.imshow("Result",stackedImage)
    
    if cv2.waitKey(1) & 0xFF == ord('m'):
        #cv2.rectangle(stackedImage, ((int(stackedImage.shape[1] / 2) - 230), int(stackedImage.shape[0] / 2) + 50),(1100, 350), (0, 255, 0), cv2.FILLED)
        cv2.putText(stackedImage, "Scan", (int(stackedImage.shape[1] / 2) - 200, int(stackedImage.shape[0] / 2)),cv2.FONT_HERSHEY_DUPLEX, 3, (0, 0, 255), 5, cv2.LINE_AA)
        cv2.imshow('Resultado final', stackedImage)
        cv2.waitKey(100)
        count += 1
        print("" , end="\n") 
        text = pytesseract.image_to_string(stackedImage,config=custom_config)
        print('\n'+text)


