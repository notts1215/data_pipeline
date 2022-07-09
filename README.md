# data pipeline
This pipeline is a simple demonstration of the processing/storage of metadata obtained from facial recognation towards ~1000 images.

## 1. Overall Architecture & tech stack used
Extraction -> Transformation -> Load -> Visualization.
<br>All scripts are written in Python3, the scheduler used is Airflow.

### 1.1 Extraction 
DataSet(image) is from Kaggle. I mixed the human face images with some non-human pictures as a whole, download+unzip the dataset and put them under a sepcific path of a server. 
##### WHAT CAN BE FURTHER DONE
I believe pulling data from the cloud is more close to PRD in practice.
<br> Alternatively, scrapy is another doable choice and I've added a sample in the code as well.

### 1.2 Transformation
By utilizing some functions via 'import cv2', one can get basic info from image sets(in this case the dataset under the path defined in step1.1)
<br>For each image, I calculate its width and height, together with a flag indicating whether a face is detected in the pic; and if detected, how many faces are there. Then combine the info with the hash value of each image(use it as a primary key) into a json format string for storage purposes. 
##### WHAT CAN BE FURTHER DONE
For this simple scenario, I used default functions in cv2. However, as mentioned in the interview, in practice one can use some new algorithms developed by Mr.Qi and other colleagues to extract more valuable info from an image.
