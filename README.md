# Data Pipeline
This pipeline is a simple demonstration of the processing/storage of metadata obtained from facial recognation towards ~1000 images.

## 1. Overall Architecture & Tech Stack used
Extraction -> Transformation -> Load -> Visualization.
<br>All scripts are written in Python3, the scheduler used is Airflow.

### 1.1 Extraction 
DataSet(image) is from Kaggle. I mocked the download operation (using url + headers) to download+unzip the dataset and put them under a sepcific path of a server, and the target path contains 1000 images.
#### WHAT CAN BE FURTHER DONE
I believe pulling data from the cloud is more close to PRD in practice.
<br> Alternatively, scrapy is another doable choice.

### 1.2 Transformation
By utilizing some functions via 'import cv2', one can get basic info from image sets(in this case the dataset under the path defined in step1.1)
<br>For each image, I calculate its width and height, together with the number of faces detected. Then combine the info with the encrypted value of each image, together with a file name (use either encrypted value or file name as a primary key) into a JSON format string for storage purposes. 
#### WHAT CAN BE FURTHER DONE
For this simple scenario, I used default functions in cv2. However, as mentioned in the interview, in practice one can use some new algorithms developed by Mr.Qi and other colleagues to extract more valuable info from an image.

### 1.3 Load
In this section, I use Hive to store data and Spark for calculation. In the DWD script, I just simply use the embedded function in Hive and separate the whole JSON value in ODS into columns respectively.
<br>**Note: This part of code only works on my current company's DEV environment (settings already well configured). As for the detail, please refer to the next section.
#### WHAT CAN BE FURTHER DONE
The output format from the previous step can be edited to reduce the redundancy of the ODS script (e.g. no need to use an external table as a transition but as the target ODS table).

### 1.4 Visualization
I performed simple visualization steps by downloading the DWD table from the data warehouse as a CSV file, using Python3/Microsoft Excel to visualize it. The plots I created include a bar chart (histogram of number of faces detected) and a pie chart (showing percentage). 
#### WHAT CAN BE FURTHER DONE
In practice, visualization is nearly the last few steps in the whole pipeline. There are several ways to achieve the goal, such as writing frontend(using Echarts, for example) + backend code and connecting to hive/impala (this is what my previous team did before); the other ways, for example, could be using CSV/XLSX file to directly visualize. My current team now using FineBI to visualize our data, it reduces manpower consumption but is constrained by functionalities (since it is an open-to-use tool).
<br> For further analysis of the data, one can figure out the relations between image size and the number of faces, for instance.


### 1.5 Schedule
I choose Airflow as the scheduler.


## 2. Uploaded file explanation
1. one script for downloading dataset (step1_extraction.py)
2. one script for image info calculation (step2_transformation.py), with a xml file for image processing algorithm.
3. two scripts for data storage & calculation (step3_load_ods.py + step3_load_dwd.py). 
<br>3.1 I uploaded the screenshot of ODS&DWD table together with the csv/xlsx file (ods_table.csv + dwd_table.xlsx).
4. one script for visualization (step4_visualization.py)
<br>4.1 Note that I also uploaded the screenshot of charts generated from 'dwd_table.xlsx'.
<br>4.2 As mentioned in 1.4, I screenshot a recently finished project on fineBI (with some info blurred), so that you can have a general picture of how it visualizes.
5. one script for scheduling (step5_schedule.py)
6. a .docx file contains screenshots mentioned.


