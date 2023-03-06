import os
from sklearn.model_selection import train_test_split
import splitfolders
import shutil

dataset = "./Dataset/e-gmd-v1.0.0/"
output = "./Dataset/MidiData/"
count = 0
input_set = output


def copy_files_from_e_gmd_to_folder():
    if not os.path.isdir(output):
        os.mkdir(output)
    for folder in os.listdir(dataset):
        if folder[0] != "d":
            continue
        for session in os.listdir(dataset + folder):
            if session == '.DS_Store':
                continue
            for files in os.listdir(dataset + folder + "/" + session):
                shutil.copy(dataset + folder + "/" + session + "/" + files, output)

def verify_length_of_newDirectory():
    og_set = set()
    new_set = set()
    old_count, new_count = 0, 0
    for file in os.listdir(output):
        new_count += 1
        new_set.add(file)
    for folder in os.listdir(dataset):
        if folder[0] != "d":
            continue
        for session in os.listdir(dataset + folder):
            if session == '.DS_Store':
                continue
            for file in os.listdir(dataset + folder + "/" + session):
                old_count += 1
                if file not in new_set:
                    print(dataset + folder + "/" + session + "/" + file)
                og_set.add(file)
    
    # print(og_set)
    print(len(og_set))
    print(old_count)
    print(new_count)
    
    print(old_count == new_count)

def correct_folder_structure_for_dataset():
    if not os.path.isdir(output + "c"):
        os.mkdir(output + "c")
    for file in os.listdir(output):
        if file == "c":
            continue
        shutil.copy(output + file, output + "c/")
        os.remove(output + file)
    count = 0
    for file in os.listdir(output + "c/"):
        count += 1
    print(count)

def split_train_test_validate():
    splitfolders.ratio(input_set, output='./Dataset/FinalData', seed=1337, ratio=(0.8, 0.1, 0.1))

def verify_length_of_new_sets():
    for folder in os.listdir("./Dataset/FinalData/"):
        if folder == ".DS_Store":
            continue
        for group in os.listdir("./Dataset/FinalData/" + folder):
            count = 0
            if group == ".DS_Store":
                continue
            for c in os.listdir("./Dataset/FinalData/" + folder + "/" + group):
                if c == ".DS_Store":
                    continue
                count += 1
            print(count)


if __name__ == "__main__":
    # copy_files_from_e_gmd_to_folder()
    # verify_length_of_newDirectory()
    # correct_folder_structure_for_dataset()
    # split_train_test_validate()
    verify_length_of_new_sets()
            
