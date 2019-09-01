# Deep Learning Workload in Serverless Computing
UROP in UC Irvine, LA, USA, December 2017 ~ February 2018

KimJeongChul
 - UCI Global Research Project 'Stanford Parser Analyze Sentences and Tree Similarity'
 - *Personal Project 'Deep Learning Workload in Serverless Computing'*
 
### Data PreProcessing(image augmentation)
 - Orchestrator
 
    > Parallel Execution : Invoke Multiple 'image_augmentation' Lambda (Concurrent Execution) using MultiProcessing Library
    
 - Image Augmentation
 
    > Download S3 File to tmp file-system which is only writable storage in Lambda
    
    > Augmentation Image file using Pillow Library(Image, ImageFilter)
    
    > Upload augmenated image to output bucket
    
### Model Training

### Model Prediction
 
 - Image Classificaiton : SqueezeNet Model Prediction
 - example : Dog Pomeranian image
 ![dog](https://user-images.githubusercontent.com/10591350/64076271-a47da280-ccfd-11e9-9e4c-8f3e6c989eb9.jpg)
 - CloudWatch Lambda logs
 ```
{
   u'toy_poodle': {'N': '0.0055214097'}, 
   u'Chihuahua': {'N': '0.11476859'}, 
   u'Pekinese': {'N': '0.06897838'}, 
   u'Pomeranian': {'N': '0.807717'}, 
   u'chow': {'N': '0.0007700342'}
} 
 ```
 ![dog_output](https://user-images.githubusercontent.com/10591350/64076286-edcdf200-ccfd-11e9-8958-c83c0e93e6ea.png)
