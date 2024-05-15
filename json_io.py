import json
import glob
import os
import win32com.client 

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
        if os.path.splitext(file)[-1] == '.lnk':
            file = get_lnk_addr(file)

        if os.path.basename(file) == fname: 
            file_list.append(file)
        elif os.path.isdir(file):
            file_list + recursive_search(file, fname, file_list)
    return file_list

def get_lnk_addr(lnk_addr):
    shell = win32com.client.Dispatch("WScript.Shell")
    shortcut = shell.CreateShortCut(lnk_addr)
    return shortcut.Targetpath
