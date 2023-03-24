import os
import shutil

home_dir_path = "C:/Users/akasliwal2/Documents/FYP/e-gmd-v1.0.0"
new_dir_path = "C:/Users/akasliwal2/Documents/FYP/wav-dataset/"

def copy_wav_files(i_path, o_path):
    if not os.path.isdir(o_path):
        os.mkdir(o_path)
    for file in os.listdir(i_path):
        if file.endswith(".wav"):
            shutil.copy(i_path + "/" + file, o_path)

if __name__ == "__main__":
    for drummer in os.listdir(home_dir_path):
        drummer_path = os.path.join(home_dir_path, drummer)
        for session in os.listdir(drummer_path):
            session_path = os.path.join(drummer_path, session)
            copy_wav_files(session_path, new_dir_path)
