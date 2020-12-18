from minio import Minio
from minio.error import (ResponseError, BucketAlreadyExists)
import os

def getMinioClient(access, secret):
    return Minio(
            'localhost:9000',
            access_key=access,
            secret_key=secret,
            secure=False
    )

def insertImage():

    if True:
        minioClient = getMinioClient('testaccess', 'testsecret')
        print('--Connected to Minio--')

        pathName = input("Enter Directory Path (start and end with slashes): ")

        try:
            entries = os.scandir(pathName)
        except OSError as error:
            print(error)
            exit('exiting...')

        extension = input("Specify file extension (include period): ")

        with os.scandir(pathName) as entries:
            path = list()
            bucket = list()
            size = list()

            bucketName = input("Choose a name for your Bucket: ")
            if (not minioClient.bucket_exists(bucketName)):
                try:
                    minioClient.make_bucket(bucketName)
                except ResponseError as identifier:
                    print("bucket name already exists.")
                    raise

            for entry in entries:
                filePath = pathName + entry.name
                if filePath.endswith(extension):
                    try:
                        with open(filePath,'rb') as testfile:
                            statdata = os.stat(filePath)
                            minioClient.put_object(
                                bucketName,
                                entry.name,
                                testfile,
                                statdata.st_size
                            )
                        path.append(entry.name)
                        bucket.append(bucketName)
                        size.append(statdata.st_size)

                    except ResponseError as identifier:
                        raise
    if not path:
        print("no images were found in the specified directory")
        exit()
    return path, bucket, size
