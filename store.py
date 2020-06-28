import os
import sys
from .config import UNIX_PATH, WINDOWS_PATH, WINDOWS_STATIC_PATH, UNIX_STATIC_PATH
import json

def get_static_path()->str:
    if sys.platform == 'linux':
        return UNIX_STATIC_PATH
    else:
        return WINDOWS_STATIC_PATH


def get_store_path()->str:
    if sys.platform == 'linux':
        return UNIX_PATH
    else:
        return WINDOWS_PATH

STORE_PATH = get_store_path()

SECURITY_FILENAME = 'security.json'

def get_security_json(path:str = STORE_PATH)->dict:
    if os.path.exists(path):
        fname = os.path.join(path,SECURITY_FILENAME)
        if os.path.isfile(fname):
            with open(fname) as json_file:
                data = json.load(json_file)
                return data
    print("No security.json file found.")
    return {}

def get_project_path(project:str, create:bool)->str:
    project_path = os.path.join(STORE_PATH, project)
    if os.path.exists(project_path):
        return project_path
    else:
        if create:
            os.mkdir(project_path)
            return project_path
        else:
            return ''

def get_class_path(project:str, class_name:str, create:bool)->str:
    project_path = get_project_path(project, create)
    class_path = os.path.join(project_path, class_name)
    if os.path.exists(class_path):
        return class_path
    else:
        if create:
            os.mkdir(class_path)
            return class_path
        else:
            return ''

CLASS_ITEM_MIN = 100

def get_new_id(project:str, class_name:str)-> int:
    class_path = get_class_path(project, class_name, False)
    max_item = CLASS_ITEM_MIN
    if os.path.isdir(class_path):
        for file in os.listdir(class_path):
            if os.path.isfile(os.path.join(class_path, file)):
                try:
                    value = int(file)
                    max_item = max(value, max_item)
                finally:
                    pass
        return max_item + 1
    else:
        return -1

def get_item_id_fname(project:str, class_name:str,item_id:int, create:bool)->str:
    return os.path.join(get_class_path(project, class_name, create), str(item_id))
