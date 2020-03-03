import pickle
import os
import subprocess
import shutil
import time
from pydub import AudioSegment
from pydub.playback import play
import random
import json

search_path = "./new_combined_phrases/"

def find_match(file_list, pattern):
    if len(pattern) == 0:
        return []
    for i in range(len(pattern),0,-1):
        if "_".join(pattern[:i]) in file_list:
            return ["_".join(pattern[:i])] + find_match(file_list, pattern[i:])
    return ["-1"]

def construct_audio2(invocation_phrase):
    available_phrases = os.listdir(search_path)
    parent_dir = "_".join(invocation_phrase.split(" "))
    if parent_dir not in available_phrases:
        return
    available_users = os.listdir(search_path+parent_dir)
    if len(available_users)==0: return
    random.shuffle(available_users)
    user_dir = search_path+parent_dir+"/"+available_users[0]
    audios = []
    for ph in invocation_phrase.split(" "):
        files = os.listdir(user_dir+"/"+ph)
        random.shuffle(files)
        for file in files:
            if ".wav" in file:
                audios.append(AudioSegment.from_wav(user_dir+"/"+ph+"/"+file))
                break
    combined_audio = audios[0]
    for i in range(1,len(audios)):
        combined_audio += AudioSegment.silent(duration=100)
        combined_audio += audios[i]
    play(combined_audio)

def main():
    construct_audio2("open honey do")

if __name__ == '__main__':
    main()