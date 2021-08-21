import boto3
import os
import logging
import json
import services.config as config


s3 = boto3.client(
	service_name='s3',
	region_name=config.S3_REGION,
	aws_access_key_id=config.AWS_S3_USER_KEY,
    aws_secret_access_key=config.AWS_S3_USER_SECRET
)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in config.ALLOWED_EXTENSIONS

def getBucket(bucketName):
    return s3.list_objects(Bucket=bucketName)

def getBucketContents(bucketName):
    res = "Bucket does not exist"
    status = 404
    try:
        bucket = getBucket(bucketName)
        if bucket.get('Contents'):
            res = json.dumps([b.get('Key') for b in bucket.get('Contents')])
            status = 200
        else:
            res = "Bucket is empty" #Value not returned with 204
            status = 204
    except Exception as e:
        logging.error(f'GetBucketContents failed: {e}')
        res = f"Error getting bucket: {bucketName}"
    return res, status

def getFileObjsFromBucket(bucket, filename=''):
    if filename and bucket.get('Contents'):
        for image in bucket.get('Contents'):
            if image.get('Key') == filename:
                return [image]
    elif bucket.get('Contents'):
        return bucket.get('Contents')
    return []

def downloadFileFromBucket(bucket, fileObject):
    fn = fileObject.get('Key')
    fp = os.path.join("temp",fn)
    if bucket.get('Name'):
        try:
            with open(fp, 'wb') as o:
                s3.download_fileobj(bucket.get('Name'), fn, o)
        except Exception as e:
            logging.error("No object of name: {} found in bucket")
    return fp

def putFileInBucket(fileName, bucket):
    try:
        result = s3.upload_file(os.path.join("temp", fileName), bucket, fileName)
    except Exception as e:
        logging.error(f'File upload failed with error: {e}')
        return f"Error uploading file: {fileName}", 404
    return f"{fileName} uploaded successfully or already present", 200

def deleteFileInBucket(fileName, bucketName):
    bucket = getBucket(bucketName)
    if getFileObjsFromBucket(bucket, filename=fileName):
        try:
            s3.delete_object(Bucket=bucketName,Key=fileName)
            res = f"{fileName} deleted successfully"
            status = 200
        except Exception as e:
            logging.error(f'File deletion failed with error: {e}')
            res = f"Error deleting file {fileName}"
            status = 404
    else:
        res = f"{fileName} not found in bucket"
        status = 404
    return res, status

	# 	for bucket in s3.buckets.
	
	# elif request.method == 'POST':
    # # Create bucket
	# 	try:
	# 		if region is None:
	# 			s3_client = boto3.client('s3')
	# 			s3_client.create_bucket(Bucket=bucket_name)
	# 		else:
	# 			s3_client = boto3.client('s3', region_name=region)
	# 			location = {'LocationConstraint': region}
	# 			s3_client.create_bucket(Bucket=bucket_name,
	# 									CreateBucketConfiguration=location)
	# 	except ClientError as e:
	# 		logging.error(e)
	# 		return False
	# 	return True
