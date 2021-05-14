from calorie import calories
from cnn_model import get_model
import os  
import cv2
import numpy as np
from sklearn.metrics import confusion_matrix



IMG_SIZE = 400
LR = 1e-3
no_of_fruits=6

MODEL_NAME = 'Fruits_dectector-{}-{}.model'.format(LR, '5conv-basic')

model_save_at=os.path.join("model",MODEL_NAME)

model=get_model(IMG_SIZE,no_of_fruits,LR)

model.load(model_save_at)
labels=['Apple','Banana','Bread','Onion','Orange','tomato']
print(labels)
test_data='apple.JPG'
img=cv2.imread(test_data)
img1=cv2.resize(img,(IMG_SIZE,IMG_SIZE))
model_out=model.predict([img1])
result=np.argmax(model_out)
name=labels[result]

cal=round(calories(result+1,img,name),2)

import matplotlib.pyplot as plt
plt.imshow(img)
plt.title('{} {} calories'.format(name,cal))
plt.axis('off')
plt.show()



