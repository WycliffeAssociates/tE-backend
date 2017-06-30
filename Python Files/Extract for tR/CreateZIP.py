# import required frameworks
import zipfile
import os

#assuming the directory path is absolute - this will work
# change this to fit your project
directory = '/Fun_With_Python/Audio'

# Create an empty array of files in the zip
filesInZip = []

# for all files, sub-folders in a directory
for subdir, dirs, files in os.walk(directory):
    # look at all the files
    for file in files:
        # store the absolute path which is is it's subdir and where the os step is
        filePath = subdir + os.sep + file

        # if the file is audio
        if filePath.endswith(".wav") or filePath.endswith(".mp3"):
            # Add to array so it can be added to the archive
            filesInZip.append(filePath.title().lower())


# using zip file create a file called zipped_file.zip
# adding the members ot filesInZip array to the compressed file
with zipfile.ZipFile('zipped_file.zip', 'w') as zipped_f:
    # for all the member in the array of files add them to the zip archive
    # doing this - this way also preserves exactly the directory location that the files sit in even before the main archive
    for members in filesInZip:
        zipped_f.write(members)