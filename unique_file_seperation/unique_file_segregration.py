# Script to find unique files by comparing 2 directory and copying the unqiue files to another directory


from os import listdir
from os.path import isfile, join
import shutil


larger_files = "./in_mixed_data"
smaller_files = "./in_local_data"
unique_folder = "./op_unique_data"

larger_files_list = [f for f in listdir(larger_files) if isfile(join(larger_files, f))]
smaller_files_list = [f for f in listdir(smaller_files) if isfile(join(smaller_files, f))]

unique_list = list(set(larger_files_list).symmetric_difference(set(smaller_files_list)))
print(unique_list)

for i in unique_list:
    print(f"copying files : {i}")
    shutil.copy(""+str(i), "")
print("Done")

