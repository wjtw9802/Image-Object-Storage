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

def getImages(entries, decision):
    minioClient = getMinioClient('testaccess', 'testsecret')
    print('--Connected to Minio--')

    while True:
        print(decision)
        if decision == 'url':
            getUrl(minioClient, entries)
            exit()
        elif decision == 'download':
            download(minioClient, entries)
            exit()
        elif decision == 'remove':
            remove(minioClient, entries)
            exit()
        else:
            print('invalid decision')
        
def getUrl(client, entries):
    print("requesting presigned url")
    files = [[i[0], i[5]] for i in entries]
    urls = []
    #method = input("specify HTTP method (get, delete, put): ")
    for obj in files:
        urls.append(client.presigned_get_object(obj[1], obj[0]))
    save = input("save to a txt? (y/n): ")
    if save == 'y':
        path = input("specify download path: ")
        with open(path, mode='wt', encoding='utf-8') as myfile:
            myfile.write('\n'.join(urls))
            myfile.write('\n')
    return files

def download(client, entries):
    path = input("specify download path: ")
    files = [[i[0], i[5]] for i in entries]
    try:
        for obj in files:
            client.fget_object(obj[1], obj[0], path+obj[0])
    except:
        print("download failed")
    print("download successful")
    return files

def remove(client, entries):
    files = [[i[0], i[5]] for i in entries]
    try:
        for obj in files:
            client.remove_object(obj[1], obj[0])
    except:
        print("remove failed")
    print("remove successful")
    return files
    