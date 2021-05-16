import sys
from win32api import GetSystemMetrics
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QPalette,QIcon,QFont
from PyQt5.QtWidgets import QMainWindow,QStyle,QPushButton,QLabel,QApplication
import TranslatorPage
import DatasetPage
import EducationPage

class Home(QMainWindow):
    def __init__(self,app): 
        super().__init__()
        self.app=app
        self.makeDarkTheme()
        
        screenWidth=GetSystemMetrics(0)
        screenHeight=GetSystemMetrics(1)             
        self.setGeometry(int(screenWidth*0.0625),int(screenHeight*0.1),int(screenWidth*0.8),int(screenHeight*0.7))    
        windowWidth=self.frameGeometry().width()
        windowHeight=self.frameGeometry().height()
        self.setFixedSize(windowWidth, windowHeight)

        

        self.setWindowTitle("Sign Language Translator")
        self.setWindowIcon(QIcon(r"Images\windowLogo.JPG"))
        
        infoButton=QPushButton(self)
        infoButton.setToolTip('<b>Release </b>v0.8.0<br><b>Model </b>v0.3.0<br><b>KODBY US</b>')
        infoButton.setIcon(self.style().standardIcon(getattr(QStyle, "SP_MessageBoxInformation")))
        infoButton.setStyleSheet("background-color:white;color:black")
        infoButton.resize(int(windowWidth*0.017),int(windowWidth*0.017))
        
        title=QLabel(self)
        title.setText("Sign Language Translator")
        title.setAlignment(Qt.AlignCenter)
        title.resize(int(windowWidth*0.3),int(windowHeight*0.075))
        title.setStyleSheet("font-size:32px;color:white;")
        title.setFont(QFont("Verdana",weight=QFont.Bold))

        
        
        translatorButton=QPushButton(self)
        translatorButton.setText("Translator")  
        translatorButton.clicked.connect(self.translatorButtonFunction)
        translatorButton.resize(int(windowWidth*0.2),int(windowHeight*0.075))
        translatorButton.setStyleSheet("font-size:24px;color:white;")

        
        
        educationButton=QPushButton(self)
        educationButton.setText("Education")
        educationButton.resize(int(windowWidth*0.2),int(windowHeight*0.075))
        educationButton.setStyleSheet("font-size:24px;color:white;")
        educationButton.clicked.connect(self.educationButtonFunction)

        
        datasetButton=QPushButton(self)
        datasetButton.setText("Dataset")
        datasetButton.resize(int(windowWidth*0.2),int(windowHeight*0.075))
        datasetButton.setStyleSheet("font-size:24px;color:white;")
        datasetButton.clicked.connect(self.datasetButtonFunction)
        datasetButton.setToolTip('<b>View Sign Language Letters!</b>')
        
        exitButton=QPushButton(self)
        exitButton.setText("Exit")
        exitButton.clicked.connect(self.exitButtonFunction)
        exitButton.resize(int(windowWidth*0.2),int(windowHeight*0.075))
        exitButton.setStyleSheet("font-size:24px;color:white;background-color: rgb(201, 26, 26);")
        
        
        kodbyUsLabel=QLabel(self)
        kodbyUsLabel.resize(int(windowWidth*0.085),int(windowHeight*0.04))
        kodbyUsLabel.setText("Powered by KODBY US")

        
        infoButton.move(int(windowWidth*0.97),int(windowHeight*0.02))
        title.move(int(windowWidth*0.38),int(windowHeight*0.2))
        translatorButton.move(int(windowWidth*0.435),int(windowHeight*0.325))
        educationButton.move(int(windowWidth*0.435),int(windowHeight*0.425))
        datasetButton.move(int(windowWidth*0.435),int(windowHeight*0.525))
        exitButton.move(int(windowWidth*0.435),int(windowHeight*0.625))
        kodbyUsLabel.move(int(windowWidth*0.90),int(windowHeight*0.95))
        

    def makeDarkTheme(self):
        self.app.setStyle("Fusion")        
        dark_palette = QPalette()
        dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.WindowText, Qt.white)
        dark_palette.setColor(QPalette.Base, QColor(25, 25, 25))
        dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ToolTipBase, Qt.white)
        dark_palette.setColor(QPalette.ToolTipText, Qt.white)
        dark_palette.setColor(QPalette.Text, Qt.white)
        dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ButtonText, Qt.white)
        dark_palette.setColor(QPalette.BrightText, Qt.red)
        dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.HighlightedText, Qt.black)
        
        self.app.setPalette(dark_palette)
        self.app.setStyleSheet("QToolTip { color: #ffffff; background-color: #2a82da; border: 1px solid white; }")
        
    def exitButtonFunction(self):
        self.app.closeAllWindows()

        
    def translatorButtonFunction(self):
        self.translatorWindow = TranslatorPage.App(self.app)
        self.translatorWindow.show()
        self.close()
        
    def datasetButtonFunction(self):
        self.datasetWindow=DatasetPage.DatasetPage()
        self.datasetWindow.show()
        
    def educationButtonFunction(self):
        self.educationWindow=EducationPage.EducationPage(self.app)
        self.educationWindow.show()
        self.close()    

if __name__=="__main__":
    app = QApplication(sys.argv)     
    homePage = Home(app)
    homePage.show()
    app.exec_()








