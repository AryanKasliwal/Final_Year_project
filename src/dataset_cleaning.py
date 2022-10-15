from genericpath import isdir
import os


if __name__ == "__main__":
    newpath = r'/Users/aryankasliwal/Documents/Cityu files/Year 4/Final_Year_Project/Dataset/EGMD' 
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    for folders in os.listdir("Dataset/e-gmd-v1.0.0"):
        if not os.path.isdir("Dataset/e-gmd-v1.0.0/" + folders):
                continue
        for more_folders in os.listdir("Dataset/e-gmd-v1.0.0/" + folders):
            if not os.path.isdir("Dataset/e-gmd-v1.0.0/" + folders + "/" + more_folders):
                continue
            for files in os.listdir("Dataset/e-gmd-v1.0.0/" + folders + "/" + more_folders):
                if files.split(".")[1] == "wav":
                    os.remove("Dataset/e-gmd-v1.0.0/" + folders + "/" + more_folders + "/" + files)
