import cv2
import os
from tensorflow.keras.layers import Flatten,Dense,Dropout,MaxPool2D,Conv2D,BatchNormalization
from keras.models import Sequential
from keras.preprocessing.image import img_to_array


class getCnnModel:
    def __init__(self):  
        modelPath=os.getcwd()+"\Resources\model.hdf5"
        
        self.model = Sequential()
        self.model.add(Conv2D(75 , (3,3) , strides = 1 , padding = 'same' , activation = 'relu' , input_shape = (28,28,1)))
        self.model.add(Dropout(0.20))
        self.model.add(BatchNormalization())
        self.model.add(MaxPool2D((2,2) , strides = 2 , padding = 'same'))
        
        self.model.add(Conv2D(50 , (3,3) , strides = 1 , padding = 'same' , activation = 'relu'))
        self.model.add(Dropout(0.25))
        self.model.add(BatchNormalization())
        self.model.add(MaxPool2D((2,2) , strides = 2 , padding = 'same'))
        
        self.model.add(Conv2D(25 , (3,3) , strides = 1 , padding = 'same' , activation = 'relu'))
        self.model.add(Dropout(0.25))
        self.model.add(BatchNormalization())
        self.model.add(MaxPool2D((2,2) , strides = 2 , padding = 'same'))
        
        self.model.add(Flatten())
        self.model.add(Dense(units = 512 , activation = 'relu'))
        self.model.add(Dropout(0.30))
        self.model.add(Dense(units = 24 , activation = 'softmax'))

        self.model.load_weights(modelPath)        
        self.model.compile(optimizer = 'adam' , loss = 'categorical_crossentropy' , metrics = ['accuracy'])
        
        
    def kerasProcessImage(self,img):
        image_x = 28
        image_y = 28
        img = cv2.resize(img, (image_x, image_y))
        img_array = img_to_array(img)
        img_array=img_array/255
        img_array = img_array.reshape(-1,28, 28, 1)
        return img_array
    

   
