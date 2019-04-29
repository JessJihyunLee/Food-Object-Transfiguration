# In[1]:
import zipfile
import os
import numpy as np
from sklearn.model_selection import train_test_split
import cv2

# In[2]:
#Here I used PaperSpace Python 3 Jupyter Notebook. I read in scraped images from local machine.
zip_ref = zipfile.ZipFile("./fooddualGAN.zip",'r')
zip_ref.extractall()
zip_ref.close()


# In[3]:
# Codes to check default directory
os.getcwd()
os.listdir('./')

# In[4]:
chicken_names = os.listdir('./foodcycleGAN/chicken_wings')
spring_names = os.listdir('./foodcycleGAN/blueberry_muffins')
train_A, test_A, train_B, test_B = train_test_split(chicken_names, spring_names, test_size=0.1, random_state=42)


# In[5]:
os.makedirs('./fooddualGAN/trainA')
os.makedirs('./fooddualGAN/trainB')
os.makedirs('./fooddualGAN/testA')
os.makedirs('./fooddualGAN/testB')

# In[6]:
f = './foodcycleGAN/chicken_wings'
l = './foodcycleGAN/blueberry_muffins'
trna = './fooddualGAN/trainA'
trnb = './fooddualGAN/trainB'
tsta = './fooddualGAN/testA'
tstb = './fooddualGAN/testB'

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
