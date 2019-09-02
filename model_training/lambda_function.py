import boto3
from tensorflow.python.keras.preprocessing import image
from tensorflow.python.keras.applications.resnet50 import preprocess_input, decode_predictions
from squeezenet import SqueezeNet
import numpy as np
import uuid

s3_client = boto3.client('s3')
tmp_path = '/tmp/'  # Writable filesystem


def train(img_local_path, label_path, model_object_key):
    model = SqueezeNet(weights='imagenet')
    img = image.load_img(img_local_path, target_size=(227, 227))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)

    label_file = open(label_path)
    y = np.array([label_file.read()])
    label_file.close()

    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])

    history = model.fit(x, y)
    model.summary()
    model.save_weights(tmp_path + model_object_key)
    return history.history


def lambda_handler(event, context):
    object_input_bucket = event['input_bucket']
    object_key = event['object_key']

    label_input_bucket = event['label_bucket']
    label_key = event['label_key']

    model_object_key = event['model_object_key']  # example : squeezenet_weights_tf_dim_ordering_tf_kernels.h5
    model_bucket = event['model_bucket']

    image_path = tmp_path + '{}{}'.format(uuid.uuid4(), object_key)
    s3_client.download_file(object_input_bucket, object_key, image_path)

    label_path = tmp_path + '{}{}'.format(uuid.uuid4(), object_key)
    s3_client.download_file(label_input_bucket, label_key, label_path)

    model_path = tmp_path + '{}{}'.format(uuid.uuid4(), model_object_key)
    s3_client.download_file(model_bucket, model_object_key, model_path)

    history = train(image_path, label_path, model_object_key)

    s3_client.upload_file(model_path, model_bucket, model_object_key)

    return history
