import pickle
import os
import subprocess
import shutil
import time
from pydub import AudioSegment
from pydub.playback import play
import random
import json

#parameters
search_path = "./new_combined_phrases/"
mfa_path = "./montreal-forced-aligner"
test_input_path = "./test_input"
test_output_path = "./test_output"

#clear test_input
def clearFolder(path):
    for file in os.listdir(path):
        os.remove(path+"/"+file)

def formatTranscript(file_path, des_path):
    a = open(file_path, "r")
    w = open(des_path, "w")
    l = a.read()
    l = l.split(",")[0]
    l.strip("/!#$%&'()*+, -./:;<=>?@[\]^_`{|}~")
    w.write(l.lower())
    a.close()
    w.close()
        
def convertToWav(path, file):
    subprocess.call(['ffmpeg', '-i', path+"/"+file,
                   path+"/"+file.split(".")[0]+".wav"])

def runMFA():
    a = subprocess.run(mfa_path+"/bin/mfa_align"+" "+test_input_path+" "+mfa_path+"/pretrained_models/eng.dict.txt"+" "+ mfa_path+"/pretrained_models/english.zip"+" "+ test_output_path,input='N',encoding='ascii',stderr=subprocess.STDOUT, shell=True)

def cutAudio(boundary, src_path, des_path):
    audio = AudioSegment.from_wav(src_path)
    trimmed_audio = audio[int(float(boundary[0])*1000):int(float(boundary[1])*1000)]
    trimmed_audio.export(des_path, format="wav")
    
def getBoundary(word, file_index):
    a = open(test_output_path+"/test_input/"+file_index+".TextGrid","r")
    lines = a.readlines()
    common = " ".join(lines)
    wl = word.split("_")
    commonl = common.split("intervals")
    bound = []
    for i, r in enumerate(commonl):
        if '"' + wl[0] + '"' in r:
            if len(wl) > 1 and '"' + wl[1] + '"' not in commonl[i+1]: continue
            index = i
            for w in wl:
                bound.append((commonl[index].split("\n")[1].split(" ")[-1], commonl[index].split("\n")[2].split(" ")[-1]))
                index = index + 1
            break
    return (bound[0][0], bound[-1][1])
    #time.sleep(50)
    #copy file to test_input
def audio_operation(test_path_audio, test_path_txt):
    clearFolder(test_input_path)
    shutil.copy2(test_path_audio, test_input_path)
    formatTranscript(test_path_txt, test_input_path+"/"+test_path_txt.split('/')[-1])
    #convert to .wav
    convertToWav(test_input_path, test_path_audio.split('/')[-1])
    #find boundary
    runMFA()
    #cut audio at boundary
    file_name = test_path_audio.split('/')[-1].split(".")[0]
    boundary = getBoundary(test_path_audio.split('/')[-2], test_path_audio.split('/')[-1].split(".")[0])
    cutAudio(boundary, test_input_path+"/"+file_name+".wav", '/'.join(test_path_audio.split('/')[:-1])+"/"+file_name+".wav")
    #paste back

def main():
	for phrase in os.listdir(search_path):
    parent_dir = search_path+phrase+"/"
    for usr in os.listdir(parent_dir):
        usr_dir = parent_dir+usr+"/"
        for ph in os.listdir(usr_dir):
            ph_dir = usr_dir+ph+"/"
            for file in os.listdir(ph_dir):
                if "flac" in file:
                    print(ph_dir+file, ph_dir+file.split(".")[0]+".txt")
                    try:
                        audio_operation(ph_dir+file, ph_dir+file.split(".")[0]+".txt")
                    except: pass

if __name__ == '__main__':
    main()