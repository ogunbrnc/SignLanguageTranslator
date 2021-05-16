import cnn_model
class Prediction:
    def __init__(self):
        self.letterList=[]
        self.probList=[]
        self.countList=[]
        self.cnnModel=cnn_model.getCnnModel()
        self.totalPredictCount=0
        self.myString=""
        
    def predictLetter(self,thresHoldedImage):
        
        maxPredictCount=75
        pred_probab, pred_class,letter = self.kerasPredict(thresHoldedImage)
        self.totalPredictCount+=1
        if self.totalPredictCount==maxPredictCount:
            self.totalPredictCount=0
            self.myString+=self.letterList[len(self.letterList)-1]
            self.clearList()
        if not self.probList:
            self.appendToList(letter,pred_probab)
            self.increasePredictCounter(letter)
        elif self.letterList.count(letter)==0 and pred_probab>=self.probList[0]:      
            if(len(self.letterList)>2):
                self.removeLastLetter()
            self.appendToList(letter,pred_probab)
            self.increasePredictCounter(letter)
        elif self.letterList.count(letter)==1:
            self.increasePredictCounter(letter)
            self.changeAccuracyProb(letter,pred_probab)  
        self.sortWithProb()   
        
    def sortWithProb(self):
        for i in range(1, len(self.probList)): 
            keyProb = self.probList[i] 
            keyLetter=self.letterList[i]
            keyCount=self.countList[i]
            j = i-1
            while j >=0 and keyProb*keyCount <= self.probList[j]*self.countList[j]: 
                    self.probList[j+1] = self.probList[j]
                    self.letterList[j+1]= self.letterList[j]
                    self.countList[j+1]=self.countList[j]
                    j -= 1
            self.probList[j+1] = keyProb 
            self.letterList[j+1]= keyLetter
            self.countList[j+1]=keyCount
     
    def increasePredictCounter(self,letter):
        for i in range(0,len(self.letterList)):
            if(self.letterList[i]==letter):
                if i>=len(self.countList):
                        self.countList.append(1)
                else:
                    self.countList[i]+=1
                
    def changeAccuracyProb(self,letter,pred_probab):
        for i in range(0,len(self.letterList)):
            if(self.letterList[i]==letter):
                self.probList[i]=((self.probList[i]*(self.countList[i]-1))+pred_probab)/self.countList[i]
                break

    def takeLetter(self,index):
        class_names = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y' ]
        return class_names[index]

    def kerasPredict(self,image):
        processed = self.cnnModel.kerasProcessImage(image)
        pred_probab = self.cnnModel.model.predict(processed)[0]
        pred_class = list(pred_probab).index(max(pred_probab))
        return max(pred_probab), pred_class,self.takeLetter(pred_class)
    
    def clearList(self):
        self.letterList.clear()
        self.probList.clear()
        self.countList.clear()
    
    def appendToList(self,letter,pred_probab):
        self.letterList.append(letter)
        self.probList.append(pred_probab)
        
    def removeLastLetter(self):
        self.letterList.pop(0)
        self.probList.pop(0)
        self.countList.pop(0)

  
        