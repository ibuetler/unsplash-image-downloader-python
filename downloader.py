#!/usr/bin/env python3

import argparse
import requests
import string
import random
import datetime, os, sys, logging, hashlib
from pathlib import Path
from os import listdir
from os.path import isfile, join

parser = argparse.ArgumentParser(description="Unsplash Downloader")
parser.add_argument('--topic', type=str, help="topic the photo shall be about", required=True)
parser.add_argument('--resolution', type=str, help="resolution of photos", required=True)
parser.add_argument('--amount', type=int, help="amount of images", required=True)
args = parser.parse_args()
topic = args.topic
resolution = args.resolution
amount = args.amount

# Create Prefix (if you run the script many times)
S=5
ran = ''.join(random.choices(string.ascii_uppercase + string.digits, k = S))

# Download an image off unsplash without the api using python

def downloadimages(search_term, resolution, amount): # Define the function to download images
    print(f"https://source.unsplash.com/random/{resolution}/?"+str(search_term)+", allow_redirects=True") # State the URL
    
    for x in range(int(amount)):                                                                                                # Loop for chosen amount of times
        response = requests.get(f"https://source.unsplash.com/random/{resolution}/?"+str(search_term)+", allow_redirects=True") # Download the photo(s)
        print("Saving to: ./photos/" + str(search_term) + "_" + ran + "_" + str(x + 1) + ".png")                                            # State the filename
        open("./photos/" + str(search_term) + "_" + ran + "_" + str(x + 1) + ".png", 'wb').write(response.content)                          # Write image file


downloadimages(topic, resolution, amount) # Call the Function

# Remove Photos with the same hash (identical files)
input_files_path = r'./photos/'
input_files = [f for f in listdir(input_files_path) if isfile(join(input_files_path, f))]
input_files = [os.path.join(input_files_path, x) for x in input_files]
inp_dups = {}
unique_inps = {}


# It calculates the hash value for each file ; decrease the block size if input file size is more
def calculate_hash_val(path, blocksize=65536):
    afile = open(path, 'rb')
    hasher = hashlib.md5()
    buf = afile.read()
    while len(buf) > 0:
        hasher.update(buf)
        buf = afile.read()
    afile.close()
    return hasher.hexdigest()


# Joins two dictionaries
def find_dups(dic_unique, dict1, dict2={}):
    for key in dict1.keys():
        if key not in dict2 and key not in dic_unique:
            dic_unique[key] = dict1[key]


# Identifying unique files
def find_unique_files(dic_unique, dict1):
    for key in dict1.keys():
        if key not in dic_unique:
            dic_unique[key] = dict1[key]



def remove_duplicate_files(all_inps, unique_inps):
    for file_name in all_inps.keys():
        if all_inps[file_name] in unique_inps and file_name!=unique_inps[all_inps[file_name]]:
            print("remove dublicate file", file_name)
            os.remove(file_name)
        elif all_inps[file_name] not in unique_inps:
            print("remove dublicate file", file_name)
            os.remove(file_name)


# main function in this file which calls all other function and process inputs

def rmv_dup_process(input_files):
    all_inps={}

    for file_path in input_files:
        if Path(file_path).exists():
           files_hash = calculate_hash_val(file_path)
           inp_dups[files_hash]=file_path
           all_inps[file_path] = files_hash
        else:
            print('%s is not a valid path, please verify' % file_path)
            sys.exit()

    find_unique_files(unique_inps, inp_dups)
    remove_duplicate_files(all_inps, unique_inps)

# remove duplicate files
rmv_dup_process(input_files)

