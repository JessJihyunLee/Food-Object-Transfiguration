import zipfile
import os
import numpy as np
from sklearn.model_selection import train_test_split
import cv2

#Here I used PaperSpace. I read in scraped images from local machine.

zip_ref = zipfile.ZipFile("./foodcycleGAN.zip",'r')
zip_ref.extractall()
zip_ref.close()
# In[2]:
os.getcwd()

# In[3]:
os.listdir('./')

# In[6]:
chicken_names = os.listdir('./foodcycleGAN/chicken_wings')
spring_names = os.listdir('./foodcycleGAN/spring_rolls')
train_A, test_A, train_B, test_B = train_test_split(chicken_names, spring_names, test_size=0.1, random_state=42)


# In[7]:
os.makedirs('./foodcycleGAN/trainA')
os.makedirs('./foodcycleGAN/trainB')
os.makedirs('./foodcycleGAN/testA')
os.makedirs('./foodcycleGAN/testB')

# In[8]:
f = './foodcycleGAN/chicken_wings'
l = './foodcycleGAN/spring_rolls'
trna = './foodcycleGAN/trainA'
trnb = './foodcycleGAN/trainB'
tsta = './foodcycleGAN/testA'
tstb = './foodcycleGAN/testB'

for i in train_A:
  t = cv2.imread(os.path.join(f,i),1)
  cv2.imwrite(os.path.join(trna,i),t)

for i in test_A:
  t = cv2.imread(os.path.join(f,i),1)
  cv2.imwrite(os.path.join(tsta,i),t)

for i in train_B:
  t = cv2.imread(os.path.join(l,i),1)
  cv2.imwrite(os.path.join(trnb,i),t)

for i in test_B:
  t = cv2.imread(os.path.join(l,i),1)
  cv2.imwrite(os.path.join(tstb,i),t)
