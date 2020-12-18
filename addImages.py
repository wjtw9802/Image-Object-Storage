import imageToMinio
import imageToSQL

print('You are about to add images')
print()

name, bucket, size = imageToMinio.insertImage()
    
print("added", len(name), "images to", bucket[0])
print()

imageToSQL.sqlConnect(name, bucket, size)