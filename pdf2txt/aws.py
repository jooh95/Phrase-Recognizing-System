import boto3
import botocore

s3 = boto3.resource('s3')
bucket_name = 'learningdatajchswm9'
bucket = s3.Bucket(bucket_name)


def exists(obj):
    try:
        s3.Object('learningdatajchswm9', obj).load()
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            return False
        else:
            # Something else has gone wrong.
            raise
    else:
        return True
