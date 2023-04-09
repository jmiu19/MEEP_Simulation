import glob
import os


fileList = glob.glob('./*.out')
if len(fileList) == 0 :
    print('no .out file')
else :
    for file in fileList :
        print(file+' removed')
        os.remove(file)

fileList = glob.glob('./output/*.mp4')
if len(fileList) == 0 :
    print('no .out file')
else :
    for file in fileList :
        print(file+' removed')
        os.remove(file)


fileList = glob.glob('./*.h5')
if len(fileList) == 0 :
    print('no .h5 file')
else :
    for file in fileList :
        print(file+' removed')
        os.remove(file)


fileList = glob.glob('./*.dat')
if len(fileList) == 0 :
    print('no .dat file')
else :
    for file in fileList :
        print(file+' removed')
        os.remove(file)
