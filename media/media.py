
import boto3
import logging
from outlet import settings
import time
import os

log = logging.getLogger(__name__)

def upload_to_s3(file, path='uploads'):
    """
    @param file: the request.FILES[something] object to upload to S3
    @param path: by default' uploads' if no intentions to change keep it like that, otherweise pass it as 'uploads/profile-pictures'
    @param return: path of file name to save in db, full link of the uploaded file
    """
    S3_BUCKET = 'simpleoutlet'
    
    s3 = boto3.resource('s3', aws_access_key_id=settings.AWS_ACCESS_KEY_ID, aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
    
    file_name, file_extension = os.path.splitext(file.name)
    new_file_name = "%s_%s%s" % (file_name, time.time(), file_extension)
    print(new_file_name)
    file_name = "%s/%s" % (path, new_file_name)
    
    bucket = s3.Bucket(S3_BUCKET)
    bucket.put_object(Key=file_name, Body=file)
        
    return new_file_name, 'https://%s.s3.amazonaws.com/%s' % (S3_BUCKET, file_name)