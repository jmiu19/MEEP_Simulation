import glob
import os


fileLists = ['./*.h5',
             './*.out',
             './*.png',
             './*.csv',
             './output/*.csv',
             './output/*.png',
             './output/*.dat',
             './output/fluxPlt/cavity_compare/freq/*.png',
             './output/fluxPlt/cavity_compare/wvlength/*.png',
             './output/fluxPlt/region_compare/freq/*.png',
             './output/fluxPlt/region_compare/wvlength/*.png',
             './output/fluxPlt/cavity_individual/freq/*.png',
             './output/fluxPlt/cavity_individual/wvlength/*.png',
             './output/fluxPlt/region_individual/freq/*.png',
             './output/fluxPlt/region_individual/wvlength/*.png',
             './output/fluxPlt/cavity_raw_freq/*.png',
             './output/fluxPlt/region_raw_freq/*.png',
             './output/resonancePlt/*.png',
             './output/animation/*.mp4',
             './output/*.out']

for name in fileLists:
    fileList = glob.glob(name)
    if len(fileList) == 0 :
        print('no '+name[-3:]+' file')
    else :
        for file in fileList :
            os.remove(file)
            print(file+' removed')
