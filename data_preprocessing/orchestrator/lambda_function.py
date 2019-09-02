import boto3
import json
from multiprocessing.dummy import Pool as ThreadPool
from functools import partial

s3 = boto3.resource('s3')
lambda_client = boto3.client('lambda')


def invoke_lambda(input_bucket, output_bucket, object_key):
    lambda_client.invoke(
        FunctionName='image_augmentation',
        InvocationType='RequestResponse',
        Payload=json.dumps({
            "input_bucket": input_bucket,
            "object_key": object_key,
            "output_bucket": output_bucket
        })
    )


def lambda_handler(event, context):
    input_bucket = event['input_bucket']
    output_bucket = event['output_bucket']

    all_object_keys = []

    for obj in s3.Bucket(input_bucket).objects.all():
        all_object_keys.append(obj.key)

    print("Number of File : " + str(len(all_object_keys)))
    print("File : " + str(all_object_keys))

    pool = ThreadPool(len(all_object_keys))
    pool.map(partial(invoke_lambda, input_bucket, output_bucket), all_object_keys)
    pool.close()
    pool.join()

    return {"num_of_file": str(len(all_object_keys))}
