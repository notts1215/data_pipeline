# data pipeline
This pipeline is a simple demonstration of the processing/storage of metadata obtained from facial recognation towards ~1000 images.

## 1. Overall Architecture & tech stack used
Extraction -> Transformation -> Load -> Visualization.
<br>All scripts are written in Python3, the scheduler used is Airflow.

### 1.1 Extraction 
DataSet(image) is from Kaggle. I mixed the human face images with some non-human pictures as a whole, download+unzip the set and put them under a sepcific path of a server. I believe pulling data from the cloud is more close to PRD in practice.
<br> Alternatively, scrapy is another doable choice and I've added a sample in the code as well.

### 1.2 Transformation

