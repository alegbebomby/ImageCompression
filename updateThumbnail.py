import boto3
import os
import sys
import uuid
from PIL import Image
import PIL.Image
import logging
import json
     
s3_client = boto3.client('s3')
log = logging.getLogger()
log.setLevel(logging.DEBUG)


def file_exist(bucket, key):
    content = client.head_object(Bucket=bucket,Key=key)
    if content.get('ResponseMetadata',None) is not None:
        log.debug("File exists {}{}".format(bucket, key))
        return True
    else:
        log.debug("File does not exists {}{}".format(bucket, key))
        return False


def resize_image(image_path, resized_path):
    with Image.open(image_path) as image:
        image.thumbnail((128, 128))
        image.save(resized_path)

def resize_image_thumbnail(image_path, resized_path):
    with Image.open(image_path) as image:
        image.thumbnail((64, 64))
        image.save(resized_path)

def handler(event, context):
    s3 = boto3.resource(service_name='s3', aws_access_key_id='AKIAW4HO5I55HYTT3ZYR', aws_secret_access_key='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')
    bucketobj = s3.Bucket('merchapp-lb-update')
    bucket = 'merchapp-lb-update'
    failed =[]
    for obj in bucketobj.objects.all():
        key = obj.key
        if not file_exist(bucket, key):
            download_path = '/tmp/{}{}'.format(uuid.uuid4(), key)
            upload_path = '/tmp/resized-{}'.format(key)
            upload_path_thumbnail = '/tmp/thumbnail-{}'.format(key)
            try:
                s3_client.download_file(bucket, key, download_path)
                resize_image(download_path, upload_path)
                s3_client.upload_file(upload_path, bucket,'resized/{}'.format(key))
                resize_image_thumbnail(download_path, upload_path_thumbnail)
                s3_client.upload_file(upload_path_thumbnail, bucket,'thumbnail/{}'.format(key))
            except:
                failed.append(key)
                print ("Error occured")
        else
            log.debug("Skip File-{}".format(key))
    
    log.debug("FailedImage {}".format(json.dumps(failed)))


