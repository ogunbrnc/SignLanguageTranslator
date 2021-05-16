from win32api import GetSystemMetrics
from PyQt5.QtWidgets import  QWidget,QLabel
from PyQt5.QtGui import QPixmap,QIcon
from PyQt5.QtCore import Qt

class DatasetPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dataset")
        self.setWindowIcon(QIcon(r"Images\windowLogo.JPG"))
        
        
        screenWidth=GetSystemMetrics(0)
        screenHeight=GetSystemMetrics(1)             
        self.setGeometry(int(screenWidth*0.0625),int(screenHeight*0.1),int(screenWidth*0.385),int(screenHeight*0.50))    
        
      
        windowWidth=self.frameGeometry().width()
        windowHeight=self.frameGeometry().height()
        self.setFixedSize(windowWidth, windowHeight)
        
        self.label=QLabel(self)
        self.label.resize(windowWidth,windowHeight)
        self.label.setAlignment(Qt.AlignCenter)     
        self.pixmap=QPixmap('Images\dataset.png')
        self.label.setPixmap(self.pixmap)
           
        
