import boto3
from PIL import Image, ImageFilter
import uuid


s3_client = boto3.client('s3')
tmp_path = '/tmp/'  # Writable filesystem


def rotate(image, download_path):
    result_path = download_path.split('.')[0] + '_rotate' + download_path.split('.')[1]
    augmentation_image = image.transpose(Image.ROTATE_90)  # Image.ROTATE_180, Image.ROTATE_270
    augmentation_image.save(result_path)
    return result_path


def filter(image, download_path):
    result_path = download_path.split('.')[0] + '_filter' + download_path.split('.')[1]
    augmentation_image = image.transpose(ImageFilter.CONTOUR)  # ImageFilter.BLUR, ImageFilter.SHARPEN
    augmentation_image.save(result_path)
    return result_path


def gray_scale(image, download_path):
    result_path = download_path.split('.')[0] + '_gray' + download_path.split('.')[1]
    augmentation_image = image.convert('L')
    augmentation_image.save(result_path)
    return result_path


def image_processing(download_path):
    upload_list = []
    with Image.open(download_path) as image:
        upload_list.append(rotate(image, download_path))
        upload_list.append(filter(image, download_path))
        upload_list.append(gray_scale(image, download_path))
    return upload_list


def lambda_handler(event, context):
    input_bucket = event['input_bucket']
    object_key = event['object_key']
    output_bucket = event['output_bucket']

    download_path = tmp_path+'{}{}'.format(uuid.uuid4(), object_key)
    s3_client.download_file(input_bucket, object_key, download_path)
    upload_list = image_processing(download_path)

    for upload_path in upload_list:
        s3_client.upload_file(upload_path, output_bucket, upload_path.split("/")[2])

    return upload_list
