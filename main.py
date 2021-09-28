import json,os,hashlib,sys,urllib.request
from shutil import copy, copyfileobj
def replace_file(destination,download_dir,source):
    if "http" in source: # download over web - otherwise assume on local disk
        temp_file = download_dir + "\\temp_file_cathy"
        with urllib.request.urlopen(source) as response, open(temp_file, 'wb') as out_file:
            copyfileobj(response, out_file)
        source = temp_file
    os.remove(destination)
    copy(source, destination)

def get_file_hash(filepath):
    with open(filepath,"rb") as f:
        b = f.read()
        return hashlib.md5(b).hexdigest()

def __main__():
    mappings = {'maps':{},'videos':{}}
    for i in range(1,10):
        mappings['maps'][str(i)] = ("\\data\\puzzle\\map\\p013_00%d.map" % i)
        mappings['videos'][str(i)] = ("\\data\movie\\%d_00.wmv" % (233+i))

    print("Performing updates according to config.json")
    with open(os.getcwd()+'\\config.json') as f:
        config = json.load(f)
    with open(os.getcwd()+'\\sources.json') as f:
        sources = json.load(f)
    steam_path = config['steam_path']
    download_dir = config['download_dir']
    made_replacements = False
    for level in config['levels'].keys():
        map_path = steam_path + mappings['maps'][level]
        vid_path = steam_path + mappings['videos'][level]
        current_map_md5 = get_file_hash(map_path)
        current_vid_md5 = get_file_hash(vid_path)
        desired_map_name = config['levels'][level]
        if current_map_md5 != sources[desired_map_name]['map_md5']:
            replace_file(map_path,download_dir,sources[desired_map_name]['map_url'])
            made_replacements = True
        if current_vid_md5 != sources[desired_map_name]['vid_md5']:
            replace_file(vid_path,download_dir,sources[desired_map_name]['vid_url'])
            made_replacements = True
    if made_replacements:
        input("Updated all maps and videos. Press Enter to close this screen.")
    else:
        input("No changes needed for maps and videos. Press Enter to close this screen.")
    

if __name__ == "__main__":
    __main__()