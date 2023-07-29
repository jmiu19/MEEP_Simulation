import glob
import os


fileLists = ['./*.h5',
             './*.out',
             './*.png',
             './*.csv',
             './output/*.csv',
             './output/*.png',
             './output/*.dat',
             './output/flux_Plt/cavity_compare/freq/*.png',
             './output/flux_Plt/cavity_compare/wvlength/*.png',
             './output/flux_Plt/region_compare/freq/*.png',
             './output/flux_Plt/region_compare/wvlength/*.png',
             './output/flux_Plt/cavity_individual/freq/*.png',
             './output/flux_Plt/cavity_individual/wvlength/*.png',
             './output/flux_Plt/region_individual/freq/*.png',
             './output/flux_Plt/region_individual/wvlength/*.png',
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
