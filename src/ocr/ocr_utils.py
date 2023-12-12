import json



def read_file_object(file_path, mode):
    with open(file_path, mode) as f:
        if mode == "r":
            return json.load(f)
        elif mode == "rb":
            return f.read()
        else :
            print("Incorrect mode to perfome action")

def write_file_object(file_path, mode, object_file):
    with open(file_path, mode) as f:
        if mode == "w" or mode == 'a':
            json.dump(object_file, f)
        else:
            print("Incorrect mode to perfome action")