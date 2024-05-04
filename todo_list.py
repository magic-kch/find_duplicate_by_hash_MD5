import hashlib
from os import listdir

dir_hash = ''
for f in listdir('files'):
    with open('files/'+f, "rb") as f:
        file_hash = hashlib.sha256()
        while chunk := f.read(8192):
            file_hash.update(chunk)
    
    dir_hash += file_hash.hexdigest()

print(hashlib.sha256(dir_hash.encode('utf8')).hexdigest())