import os

def rename_files():
    #(1) get the file names from a folder
    file_list = os.listdir(r"C:\Users\shary\Documents\GitHub\udacity_fullstack\module_one\lesson_1\secret")

    # manage the current working directory
    saved_path = os.getcwd()
    print("Current working directory is " + saved_path)
    os.chdir(r"C:\Users\shary\Documents\GitHub\udacity_fullstack\module_one\lesson_1\secret")

    #(2) for each file, rename filename
    for file_name in file_list :
        os.rename(file_name, file_name.strip("0123456789"))
    os.chdir(saved_path)

rename_files()
