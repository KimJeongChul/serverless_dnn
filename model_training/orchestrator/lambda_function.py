import boto3
import json
from multiprocessing.dummy import Pool as ThreadPool
from functools import partial

s3 = boto3.resource('s3')
lambda_client = boto3.client('lambda')


def invoke_lambda(object_input_bucket, label_input_bucket, model_bucket, model_object_key, object_key):
    lambda_client.invoke(
        FunctionName='train_model',
        InvocationType='RequestResponse',
        Payload=json.dumps({
            "input_bucket": object_input_bucket,
            "object_key": object_key,
            "label_bucket": label_input_bucket,
            "label_key": object_key,
            "model_bucket": model_bucket,
            "model_object_key": model_object_key

        })
    )


def lambda_handler(event, context):
    object_input_bucket = event['input_bucket']
    label_input_bucket = event['label_bucket']
    model_bucket = event['model_bucket']
    model_object_key = event['model_object_key']  # example : squeezenet_weights_tf_dim_ordering_tf_kernels.h5

    all_object_keys = []

    for obj in s3.Bucket(object_input_bucket).objects.all():
        all_object_keys.append(obj.key)

    print("Number of File : " + str(len(all_object_keys)))
    print("File : " + str(all_object_keys))

    pool = ThreadPool(len(all_object_keys))
    pool.map(partial(invoke_lambda, object_input_bucket,
                     label_input_bucket, model_bucket, model_object_key), all_object_keys)
    pool.close()
    pool.join()

    return {"num_of_file": str(len(all_object_keys))}
