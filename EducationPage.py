import cv2
from win32api import GetSystemMetrics
from PyQt5.QtWidgets import  QWidget, QLabel,QStyle,QListWidget,QProgressBar,QPushButton,QListWidgetItem,QHBoxLayout,QToolButton
from PyQt5.QtGui import QIcon,QPixmap,QImage
from PyQt5.QtCore import Qt, pyqtSlot
import numpy as np
import getvideocapture
import HomePage

class EducationPage(QWidget):
    def __init__(self,app):
        super().__init__()
        self.app=app
        self.setWindowIcon(QIcon(r"Images\windowLogo.JPG"))
        self.setWindowTitle("Education")
        
        self.list=QListWidget(self)
        self.isButtonClicked=False
        self.targetPredictedLetterStr=str()
        self.initializeLetterList()
        self.colorList=["yellow","red","green"]
        
           
        

        self.predictedText=QLabel(self)
        self.predictedInfoLabel=QLabel(self)
        self.targetPredictImageInfoLabel=QLabel(self)

        self.progressBar=QProgressBar(self)
                
        screenWidth=GetSystemMetrics(0)
        screenHeight=GetSystemMetrics(1)       
    
        windowWidthCoordinates=[int(screenWidth*0.0625),int(screenWidth*0.8)]
        windowHeightCoordinates=[int(screenHeight*0.1),int(screenHeight*0.7)]
        self.setGeometry(windowWidthCoordinates[0],windowHeightCoordinates[0],windowWidthCoordinates[1],windowHeightCoordinates[1])
        windowHeightLength=windowHeightCoordinates[1]-windowHeightCoordinates[0]
        windowWidthLength=windowWidthCoordinates[1]-windowWidthCoordinates[0]
        
        self.setFixedSize(windowWidthLength*1.08, windowHeightLength*1.2)

        self.cameraWidth = windowWidthLength
        self.cameraHeight = windowHeightLength*0.9

        self.cameraFrame = QLabel(self)
        self.cameraFrame.resize(self.cameraWidth, self.cameraHeight)
        self.cameraFrame.move(windowWidthLength*0.01, windowHeightLength*0.02)
        
        
        infoButton=QPushButton(self)
        infoButton.setToolTip('<b>Release </b>v0.8.0<br><b>Model </b>v0.3.0<br><b>KODBY US</b>')
        infoButton.setIcon(self.style().standardIcon(getattr(QStyle, "SP_MessageBoxInformation")))
        infoButton.setStyleSheet("background-color:white;color:black")
      
        
        howToButton=QPushButton( self)
        howToButton.setIcon(self.style().standardIcon(getattr(QStyle, "SP_MessageBoxQuestion")))
        howToButton.setToolTip('<b>*You need to select a letter from the letter list.<br>'
                               +'*You can see the letter and image of the letter at bottom-right area after selecting.<br>'
                               +'*You can understand your hand sign is wrong or correct by check bottom-left area.<br></b>')
        
        
        
        
        howToButton.setStyleSheet("background-color:white;color:black")
        
        backButton=QPushButton(self)
        backButton.setIcon(self.style().standardIcon(getattr(QStyle, "SP_DialogOkButton")))
        backButton.clicked.connect(self.backToHome)
        backButton.setStyleSheet("background-color:white")
 
        
        
        self.progressBar.move(windowWidthLength*0.6, windowHeightLength*0.1)
        self.progressBar.resize(screenWidth-windowWidthLength*0.9, screenHeight-windowHeightLength*1.6)
        self.progressBar.setStyleSheet("QProgressBar::chunk ""{""background-color: green;text-align:center""}")
        self.progressBar.setAlignment(Qt.AlignCenter)
        
        self.predictedLetterInfo=QLabel(self)
        self.predictedLetterInfo.move(windowWidthLength*0.6,windowHeightLength*0.15)
        self.predictedLetterInfo.setText("Predicted Letters:")
        self.predictedLetterInfo.setStyleSheet("color:white;font-size:36px;")
        self.predictedLetterInfo.resize(windowWidthLength*0.2,windowHeightLength*0.15)

        
        self.firstPredictedLetter=QLabel(self)
        self.firstPredictedProbability=QLabel(self)
        self.firstPredictedLetter.move(windowWidthLength*0.6,windowHeightLength*0.275)
        self.firstPredictedProbability.move(windowWidthLength*0.6,windowHeightLength*0.325)
        self.firstPredictedLetter.setStyleSheet("background-color: rgba(255, 255, 255, 10);")
        self.firstPredictedProbability.setStyleSheet("color:white;font-size:18px;")
        self.firstPredictedLetter.setAlignment(Qt.AlignCenter)
        self.firstPredictedProbability.setAlignment(Qt.AlignCenter)
        self.firstPredictedProbability.resize(windowWidthLength*0.07,windowHeightLength*0.15)
        self.firstPredictedLetter.resize(windowWidthLength*0.07,windowHeightLength*0.15)

        self.secondPredictedLetter=QLabel(self)
        self.secondPredictedProbability=QLabel(self)
        self.secondPredictedLetter.move(windowWidthLength*0.75,windowHeightLength*0.275)
        self.secondPredictedProbability.move(windowWidthLength*0.75,windowHeightLength*0.325)
        self.secondPredictedLetter.setStyleSheet("background-color: rgba(255, 255, 255, 10);")
        self.secondPredictedProbability.setStyleSheet("color:white;font-size:18px;")
        self.secondPredictedLetter.setAlignment(Qt.AlignCenter)
        self.secondPredictedProbability.setAlignment(Qt.AlignCenter)
        self.secondPredictedProbability.resize(windowWidthLength*0.07,windowHeightLength*0.15)
        self.secondPredictedLetter.resize(windowWidthLength*0.07,windowHeightLength*0.15)

        self.thirdPredictedLetter=QLabel(self)
        self.thirdPredictedProbability=QLabel(self)
        self.thirdPredictedLetter.move(windowWidthLength*0.9,windowHeightLength*0.275)
        self.thirdPredictedProbability.move(windowWidthLength*0.9,windowHeightLength*0.325)
        self.thirdPredictedLetter.setStyleSheet("background-color: rgba(255, 255, 255, 10);")
        self.thirdPredictedProbability.setStyleSheet("color:white;font-size:18px;")
        self.thirdPredictedLetter.setAlignment(Qt.AlignCenter)
        self.thirdPredictedProbability.setAlignment(Qt.AlignCenter)
        self.thirdPredictedProbability.resize(windowWidthLength*0.07,windowHeightLength*0.15)
        self.thirdPredictedLetter.resize(windowWidthLength*0.07,windowHeightLength*0.15)


        self.predictedLetterList=[self.firstPredictedLetter,self.secondPredictedLetter,self.thirdPredictedLetter]
        self.predictedProbabilityList=[self.firstPredictedProbability,self.secondPredictedProbability,self.thirdPredictedProbability]

        
        self.list.move(windowWidthLength*0.6,windowHeightLength*0.45)
        self.list.resize(screenWidth-windowWidthLength*0.9,screenHeight-windowHeightLength*1.2)
    
        
        self.predictedInfoLabel.setText("Predicted Text:")
        self.predictedInfoLabel.setStyleSheet("color:white; font-size:24px;")
        self.predictedInfoLabel.move(windowWidthLength*0.01,windowHeightLength*0.95)


        self.predictedText.move(windowWidthLength*0.01,windowHeightLength)
        self.predictedText.resize(windowWidthLength*0.55,windowHeightLength*0.1)
        self.predictedText.setAlignment(Qt.AlignCenter)
        self.predictedText.setStyleSheet("background-color: rgba(255, 255, 255, 10); color:white; font-size:32px;")

        
        
        self.targetPredictImageInfoLabel.setText("Target Predict Image:")
        self.targetPredictImageInfoLabel.setStyleSheet("color:white; font-size:24px;")
        self.targetPredictImageInfoLabel.move(windowWidthLength*0.6,windowHeightLength*0.95)
        
        self.targetPredictImage=QLabel(self)
        self.targetPredictImage.setStyleSheet("background-color: rgba(255, 255, 255, 10);")
        self.targetPredictImage.resize(windowWidthLength*0.07,windowHeightLength*0.15)
        self.targetPredictImage.setAlignment(Qt.AlignCenter)   
        self.targetPredictImage.move(windowWidthLength*0.65,windowHeightLength)
        

        self.targetPredictLetterInfoLabel=QLabel(self)
        self.targetPredictLetterInfoLabel.setText("Target Predict Letter:")
        self.targetPredictLetterInfoLabel.setStyleSheet("color:white; font-size:24px;")
        self.targetPredictLetterInfoLabel.move(windowWidthLength*0.85,windowHeightLength*0.95)
        
        
        self.targetPredictLetter=QLabel(self)
        self.targetPredictLetter.move(windowWidthLength*0.9,windowHeightLength)
        self.targetPredictLetter.setStyleSheet("color:black;font-size:32px;background-color: rgba(255, 255, 255, 10);")
        self.targetPredictLetter.setAlignment(Qt.AlignCenter)
        self.targetPredictLetter.resize(windowWidthLength*0.07,windowHeightLength*0.15)
        
    
        self.thread = getvideocapture.getVideoCapture()
        self.thread.change_pixmap_signal.connect(self.update_image)
        self.thread.start()

   
    
        infoButton.move(int(windowWidthLength*1.05),int(windowHeightLength*0.02))
        howToButton.move(windowWidthLength*1.025,windowHeightLength*0.02)
        backButton.move(windowWidthLength,windowHeightLength*0.02)        
       

    def closeEvent(self, event):
        self.thread.stop()
        event.accept()


    @pyqtSlot(np.ndarray)
    def update_image(self, cv_img):
        """Updates the image_label with a new opencv image"""
        if self.thread.isHandInRectangle==True:
            if(self.isButtonClicked==True):
                self.startProgressBar()
                self.predictedLetter,self.predictedProb,self.predictedCount=self.thread.getPredictedLetterAccuracyAndCount()    
                self.setPredictedText()
                self.clearList()            
                lenOfPredictedLetter=len(self.predictedLetter)
                probabilitySum=0         
                for count in range(lenOfPredictedLetter):
                    probabilitySum+=self.predictedCount[count]*self.predictedProb[count] 
                for count in range(lenOfPredictedLetter):
                    self.predictedLetterList[count].setText(self.predictedLetter[count])
                    self.predictedLetterList[lenOfPredictedLetter-count-1].setStyleSheet("color:"+self.colorList[count-1]+";font-size:32px;background-color: rgba(255, 255, 255, 10);")
                    formattedPredAccuracy=format(round(self.predictedCount[count]*self.predictedProb[count]/probabilitySum,2)*100,'.2f')
                    self.predictedProbabilityList[count].setText(str(formattedPredAccuracy)+"%")
            else:
                self.predictedText.setText("Please, choose what do you want to predict!")    
        else:
            self.stopProgressBar()               
        qt_img = self.convert_cv_qt(cv_img)
        self.cameraFrame.setPixmap(qt_img)

    def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(self.cameraWidth, self.cameraHeight, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)
    
    def initializeLetterList(self):
        letterList = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y' ]
        for i in range(len(letterList)):
                self.addButtonList(letterList[i])      

    def addButtonList(self,text):
        item = QListWidgetItem(text)
        item.setTextAlignment(Qt.AlignCenter)
        self.list.addItem(item)  
        widget = QWidget(self.list)
        button = QToolButton(widget)
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addStretch()
        layout.addWidget(button)
        self.list.setItemWidget(item, widget)
        button.clicked.connect(
            lambda: self.handleButtonClicked(text))
        
    def handleButtonClicked(self, item):
        self.targetPredictedLetterStr=item
        self.initializePredictLetterAndLetterImage(self.targetPredictedLetterStr)
        self.isButtonClicked=True

    def initializePredictLetterAndLetterImage(self,letter):
        self.targetPredictLetter.setText(letter)
        absolutePath=r"Images\Letters\\"+letter+".JPG"
        self.pixmap=QPixmap(absolutePath)
        self.targetPredictImage.setPixmap(self.pixmap)
        
    def startProgressBar(self):      
        self.progressBar.setValue(int(self.thread.getTotalPredictCount()*1.3))
    
    def stopProgressBar(self):
        self.progressBar.setValue(0)

    def backToHome(self):
        self.homeWindow = HomePage.Home(self.app)
        self.homeWindow.show()
        self.close()
        
    def clearList(self):
        for count in range(len(self.predictedLetterList)):
            self.predictedLetterList[count].clear()
            self.predictedProbabilityList[count].clear()

    def setPredictedText(self):
        lenPredictedLetterList=len(self.predictedLetter)
        if lenPredictedLetterList!=0 and self.predictedLetter[lenPredictedLetterList-1]==self.targetPredictedLetterStr:
            self.predictedText.setStyleSheet("background-color: rgba(255, 255, 255, 10); color:green; font-size:32px;")
            self.predictedText.setText("Correct!")   
        else:
            self.predictedText.setStyleSheet("background-color: rgba(255, 255, 255, 10); color:red; font-size:32px;")
            self.predictedText.setText("Not Correct!")    


       
         



        
        
  

