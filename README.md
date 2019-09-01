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