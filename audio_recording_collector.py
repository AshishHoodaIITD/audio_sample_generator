import subprocess
import os
from shutil import copyfile
import shutil
import random

#parameters
extentions_to_search = "{csv}"
path_to_dataset = "/speech_datasets/common_voice/"
audio_sample_directory = "./new_combined_phrases/"

def create_phrase_map(records, search_phrases):
	phrase_record = {}
	search_phrases = [s.strip(".") for s in search_phrases]
	search_phrases = [s[:-1] if s.endswith("\n") else s for s in search_phrases]

	for rec in records:
	    for sph in search_phrases:
	        if " "+sph.lower()+" " in rec.lower() or " "+sph.lower()+"\n" in rec.lower():
	            sph = sph.lower()
	            num = rec.split("/")[6]
	            if num not in phrase_record:
	                phrase_record[num] = {}
	            if sph not in phrase_record[num]:
	                phrase_record[num][sph] = []
	            phrase_record[num][sph].append(rec)
	return phrase_record

def create_user_audio_map(combined_phrases, phrase_record):
	phrase_to_user = {}
	for cc in combined_phrases:
	    phrase_to_user[cc] = {}
	    words = cc.split(" ")
	    phrase_list = list(phrase_record.keys())
	    random.shuffle(phrase_list)
	    count = 0
	    for num in phrase_list:
	        f = 0
	        for w in words:
	            if w not in phrase_record[num]:
	                f=1
	                break
	        temp_dict = {}
	        if f==0:
	            for w in words:
	                temp_dict[w] = phrase_record[num][w]
	            phrase_to_user[cc][num] = temp_dict
	            count+=1
	            if count>5: break
	return phrase_to_user

def create_audio_directories(phrase_to_user):
	for k in list(phrase_to_user.keys()):
	    phrase_folder = audio_sample_directory+"_".join(str(k).split(" "))
	    os.mkdir(phrase_folder)
	    for usr, li in phrase_to_user[k].items():
	        user_folder = audio_sample_directory+"_".join(str(k).split(" "))+"/"+usr
	        os.mkdir(user_folder)
	        for ph, l in li.items():
	            ph_folder = audio_sample_directory+"_".join(str(k).split(" "))+"/"+usr+"/"+ph
	            os.mkdir(ph_folder)

def copy_audio_recordings(phrase_to_user):
	for k in list(phrase_to_user.keys()):
	    phrase_folder = audio_sample_directory+"_".join(str(k).split(" "))
	    for usr, li in phrase_to_user[k].items():
	        user_folder = audio_sample_directory+"_".join(str(k).split(" "))+"/"+usr
	        for ph, l in li.items():
	            ph_folder = audio_sample_directory+"_".join(str(k).split(" "))+"/"+usr+"/"+ph
	            for rec in l:
	                source_path = rec.split(":")[0].split(".")[0] + "-" + rec.split(":")[2].split(" ")[0].split("-")[-1]+".flac"
	                des_path = ph_folder + "/" + source_path.split("/")[-1]
	                if source_path.split("/")[-1] not in os.listdir(ph_folder):
	                    shutil.copy2(source_path, des_path)
	                w = open(ph_folder+"/"+source_path.split("/")[-1].split(".")[0]+".txt", "w")
	                w.write(rec.split(":")[-1])
	                w.close()

def main():
	subprocess.run(["./search_records.sh", extensions_to_search, path_to_dataset])

	r = open("results.txt","r")
	records = r.readlines()

	r = open("combined_phrases.txt","r")
	combined_phrases = r.readlines()
	combined_phrases = [s.strip(".") for s in combined_phrases]
	combined_phrases = [s[:-1] if s.endswith("\n") else s for s in combined_phrases]

	r = open("search_phrases.txt","r")
	search_phrases = r.readlines()

	phrase_record = create_phrase_map(records, search_phrases)
	phrase_to_user = create_user_audio_map(combined_phrases, phrase_record)
	create_audio_directories(phrase_to_user)
	copy_audio_recordings(phrase_to_user)

if __name__ == '__main__':
    main()
