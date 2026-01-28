import os
import requests
import re
import time
from storageid import API_Key #Fetch API_Key
import traceback

dir = os.getcwd()


class SteamFetchPublishedFiles:
    def __init__(self, api_key): 
        self.api_key = api_key
        self.baseurl = "https://api.steampowered.com/" 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Initial API Request

    def fetchfileinfo(self, fileid):
        endpoint = f"{self.baseurl}ISteamRemoteStorage/GetPublishedFileDetails/v1/"
        parameters = {
            'itemcount' : 1,
            'publishedfileids[0]' : fileid
                  }
        response = requests.post(endpoint, data=parameters, params={'key': self.api_key})
        return response.json()
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Fetch File details -> JSON


def is_workshop_foler(folder_name):
    patterns_folder=[
        r'^workshop_\d+',
        r'^workshop\d+',
        r'^\d{6,}$',
        r'^mod_\d+',
        r'^\d+_.+',
        r'^workshopcontent_\d+',
        r'^workshopcontent\d+',
        r'^\d{6,} Not Found'
    ] # patterns

    for pattern_folder in patterns_folder: 
        if re.match(pattern_folder, folder_name): #if any pattern match, it considers the folder as a workshop folder
            return True #Hence the True bool
        
    return False #False, if its out of the pattern
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Check if its a steam folder or not


def fetch_id(folder_name):
    match = re.search(r'\d{6,}', folder_name)
    return match.group(0) if match else None
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Fetch fileid from folder name


def get_title(fileid):
    try:
        fetchmain = API.fetchfileinfo(fileid) #API From StorageID.py
        details = fetchmain.get('response', {}).get('publishedfiledetails', [{}])[0]

        if details.get('result') == 1:
            Title = details.get('title', fileid)
            Title = re.sub(r'[<>:"/\\|?*]', '', Title).strip()
            return Title
        
    except Exception as e:
        print(f"Error fetching metadata for {fileid}: {e}")
    
    return f"{fileid} Not Found"
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Fetch and Sanitize Title 


API = SteamFetchPublishedFiles(API_Key)# Initialize Class
items = os.listdir(dir)
Folder_Count = 0
Workshop_Folder_Count = 0


for item in items:
    fullpath = os.path.join(dir, item)
    if os.path.isdir(fullpath):
        Folder_Count += 1

        if is_workshop_foler(item):
            Workshop_Folder_Count += 1

            fileid = fetch_id(item)
            Title = get_title(fileid)
            newpath = os.path.join(dir, Title)

            if item == Title:
                continue

            newpath = os.path.join(dir, Title)
    
    # Avoid overwriting existing folders
            if os.path.exists(newpath):
                newpath = os.path.join(dir, f"{Title}_{fileid}")

            try:
                os.rename(fullpath, newpath)
                print (f"Renamed {item} to {Title}")
            except Exception as e:
                print(f"Failed to rename {item} to {Title}")
                traceback.print_exc()

time.sleep(0.5)