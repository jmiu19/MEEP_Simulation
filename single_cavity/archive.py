import glob
import shutil
import os

folder = input('new folder name: ')
origin = 'output/'
target = 'previous_output/'+folder+'/'
other_files = ['./*.h5', './*.csv']

# Fetching the list of all the files
files = os.listdir(origin)

if not os.path.exists('previous_output/'+folder):
    os.makedirs('previous_output/'+folder)


# Fetching all the files to directory
for file_name in files:
    try:
        shutil.copytree(origin+file_name, target+file_name)
    except:
        shutil.copy(origin+file_name, target+file_name)
for file_names in other_files:
    files = glob.glob(file_names)
    for file_name in files:
        shutil.copy(file_name, target+file_name)
print("Files are copied successfully")
