import json
import glob
import os

def write_json(fname, **kwargs):
    json_string = json.dumps(kwargs, indent=4)
    with open(fname,'w') as f:
        f.write(json_string)

def read_json(fname):
    with open(fname, 'r') as f:
        data = json.load(f)
    return data

def recursive_search(addr: str, fname: str, file_list: list) -> list:
    files = glob.glob(addr+'/*') + glob.glob(addr+'/.*')
    for file in files:
        if os.path.basename(file) == fname: 
            file_list.append(file)
        elif os.path.isdir(file):
            file_list + recursive_search(file, fname, file_list)
    return file_list

