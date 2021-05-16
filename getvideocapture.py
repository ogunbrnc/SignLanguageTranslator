import cv2
import numpy as np
import prediction
import didyoumean
from PyQt5.QtCore import pyqtSignal, QThread

class getVideoCapture(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)
    def __init__(self):
        super().__init__()
        self._run_flag = True
        self.isHandInRectangle=False
        self.didYouMean=didyoumean.didYouMean()
        self.prediction=prediction.Prediction()       
    def run(self):
        optimumThresholdValue=2500
        self.cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
        while self._run_flag:           
           self.createRectangleOnVideo()
           croppedImage = self.getImageOnRectangle()
           extractedSkin=self.extractSkin(croppedImage)
           contours,thresHoldedImage=self.preprocessImage(croppedImage,extractedSkin)
           
           if self.checkHandInRectangle(contours):
               targetOfImage= max(contours,key=lambda x: cv2.contourArea(x))
               if cv2.contourArea(targetOfImage) > optimumThresholdValue:         
                   self.prediction.predictLetter(thresHoldedImage)
           else:
               self.prediction.totalPredictCount=0
               if self.prediction.letterList:
                   self.prediction.clearList()

           if self.ret:
                self.change_pixmap_signal.emit(self.img)
        self.cap.release()           
    def createRectangleOnVideo(self):
        start_point=(300,300)
        end_point=(100,100)
        color=(0,255,0)
        thickness=0
        self.ret, self.img = self.cap.read()
        
        self.img = cv2.flip(self.img, 1)    
        cv2.rectangle(self.img,start_point,end_point,color,thickness)
        
    def getImageOnRectangle(self):
        start_point=(300,300)
        end_point=(100,100)
        return self.img[end_point[0]:start_point[0],end_point[0]:start_point[0]]
    
    def extractSkin(self,croppedImage):
        lowerSkinColor = np.array([0,58,50], dtype=np.uint8)
        upperSkinColor = np.array([30,255,255], dtype=np.uint8)
        hsv = cv2.cvtColor(croppedImage, cv2.COLOR_BGR2HSV)
        return cv2.inRange(hsv, lowerSkinColor, upperSkinColor)
        
    def preprocessImage(self,croppedImage,extractedSkin):
        grayedImage=cv2.cvtColor(croppedImage,cv2.COLOR_BGR2GRAY)    
        bluredImage=cv2.GaussianBlur(grayedImage,(5,5),2)
        thresHoldedImage = cv2.adaptiveThreshold(bluredImage,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,11,2)
        _, thresHoldedImage = cv2.threshold(thresHoldedImage, 70, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
        contours,hierarchy=cv2.findContours(extractedSkin.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        
        return contours,thresHoldedImage
   
        
    def checkHandInRectangle(self,contours):
        if len(contours)>0:
            self.isHandInRectangle=True
            return self.isHandInRectangle
        self.isHandInRectangle=False
        return self.isHandInRectangle
           
    def preProcessDidYouMean(self,sentence):
        wordList=sentence.split()
        return wordList[-1]

    
    def changeWord(self,word):
        if(word!=""):
            wordList=self.prediction.myString.split()
            withoutLastWord=wordList[:-1]
            self.prediction.myString=' '.join([str(i) for i in withoutLastWord])
            self.prediction.myString+=' '+word
            
    def stop(self):
        self._run_flag = False
        self.wait()

        
    def didYouMeanCorrection(self):
        spellWord=self.preProcessDidYouMean(self.prediction.myString)
        candidatesList=self.didYouMean.correction(spellWord,self.img)
        return candidatesList
    def backSpace(self):
        self.prediction.myString=self.prediction.myString[:-1]
    
    def space(self):
        self.prediction.myString+=' '
        
    def getMyString(self):
        return self.prediction.myString
        
    def setMyString(self,letter):
        if letter!='':
            self.prediction.myString+=letter
            self.prediction.totalPredictCount=0
            self.prediction.clearList()
    
    def getTotalPredictCount(self):
        return self.prediction.totalPredictCount
    
    def getPredictedLetterAccuracyAndCount(self):
        return self.prediction.letterList,self.prediction.probList,self.prediction.countList
