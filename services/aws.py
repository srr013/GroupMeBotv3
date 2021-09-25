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
            contents = [b.get('Key') for b in bucket.get('Contents')]
            returnValues = {}
            # raise Exception
            for item in contents:
                item = item.split("/")
                i = 0
                pointer = returnValues
                while i < len(item):
                    if not pointer.get(item[i], None):
                        pointer[item[i]] = {}
                    if i == len(item) - 2:
                        if isinstance(pointer[item[i]], list):
                            pointer[item[i]].append(item[i+1])
                        else:
                            pointer[item[i]] = [item[i+1]]
                        break
                    else:
                        pointer = pointer[item[i]]
                        i += 1
            res = returnValues
            status = 200
        else:
            res = "Bucket is empty" #Value not returned with 204
            status = 204
    except Exception as e:
        logging.error(f'GetBucketContents failed: {e}')
        res = f"Error getting bucket: {bucketName}"
    return res, status

def getGroupFileObjsFromBucket(bucket, groupId, directory='',filename=''):
    contents = []
    if filename and bucket.get('Contents'):
        for s3File in bucket.get('Contents'):
            s3FilePath = s3File.get('Key').split("/")
            if len(s3FilePath) == 3 and directory:
                if s3FilePath[0] == groupId:
                    if s3FilePath[1] == directory:
                        if s3FilePath[2].lower() == filename.lower():
                            contents = [s3File]
    elif bucket.get('Contents'):
        for s3File in bucket.get('Contents'):
            s3FilePath = s3File.get('Key').split("/")
            if s3FilePath[0] == groupId:
                contents.append(s3File)
    else:
        logging.error(f'Bucket has no "Contents" key')
    return contents

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
        #only filenames that are passed through
        path = fileName.split("_")
        fileName = fileName.replace("_", "/")
        result = s3.upload_file(os.path.join(config.UPLOAD_FOLDER, *path), bucket, fileName)
    except Exception as e:
        logging.error(f'File upload failed with error: {e}')
        return f"Error uploading file: {fileName}", 404
    return f"{fileName} uploaded successfully or already present", 200

def deleteFileInBucket(fileName, bucketName):
    bucket = getBucket(bucketName)
    # if getGroupFileObjsFromBucket(bucket, filename=fileName):
    try:
        s3.delete_object(Bucket=bucketName,Key=fileName)
        res = f"{fileName} deleted successfully"
        status = 200
    except Exception as e:
        logging.error(f'File deletion failed with error: {e}')
        res = f"Error deleting file {fileName}"
        status = 404
    # else:
    #     res = f"{fileName} not found in bucket"
    #     status = 404
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
