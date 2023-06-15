import glob
import os


fileLists = ['./*.h5',
             './*.out',
             './*.png',
             './output/*.png',
             './output/*.dat',
             './output/*.mp4',
             './output/*.out']

for name in fileLists:
    fileList = glob.glob(name)
    if len(fileList) == 0 :
        print('no '+name[-3:]+' file')
    else :
        for file in fileList :
            print(file+' removed')
            os.remove(file)