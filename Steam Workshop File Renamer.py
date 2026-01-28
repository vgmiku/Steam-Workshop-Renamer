import os
import requests
import re
import json

class SteamFetchPublishedFiles:
    def __init__(self, api_key): 
        self.api_key = api_key
        self.baseurl = "https://api.steampowered.com/" 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Initial API Request

    def fetchfileinfo(self, fileid):
        WorkshopRemoteStorage = f"{self.baseurl}ISteamRemoteStorage/GetPublishedFileDetails/v1/"
        parameters0 = {
            'key': self.api_key,
            'itemcount' : 1,
            'publishedfileids[0]' : fileid
                  }
        response = requests.post(WorkshopRemoteStorage, data=parameters0)
        return response.json()
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Fetch File details -> JSON

dir = os.getcwd()

def is_workshop_foler(folder_name):
    patterns_folder=[
        r'^workshop_\d+',
        r'^workshop\d+',
        r'^\d{6,}$',
        r'^mod_\d+',
        r'^\d+_.+',
        r'^workshopcontent_\d+',
        r'^workshopcontent\d+',
    ] # patterns

    for pattern_folder in patterns_folder: 
        if re.match(pattern_folder, folder_name): #if any pattern match, it considers the folder as a workshop folder
            return True #Hence the True bool
        
    return False #False, if its out of the pattern
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Check if its a steam folder or not


def fetch_id(folder_name):
    Digits_in_folder = re.findall(r'\d+', '', )
    if Digits_in_folder:
        id = max(Digits_in_folder, key=len)
        if id:
            len(id) >= 6
            return id
        return None



def get_title(fileid):
    from storageid import API_Key
    API = SteamFetchPublishedFiles(API_Key)
    fetchmain = API.fetchfileinfo(fileid)
    Fetchdata = fetchmain.get('response', {})
    datalist = Fetchdata.get('publishedfiledetails', [{}])
    Title = datalist[0].get('title', f"{fileid} Not Found")
    Title = re.sub(r'[/;\!@#$%^&*()=]', '', Title)
    return Title
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Fetch and Sanitize Title 