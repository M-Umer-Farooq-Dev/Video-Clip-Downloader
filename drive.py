import requests
import pandas as pd
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip 
import os


def download_file_from_google_drive(id, destination):
    URL = "https://docs.google.com/uc?export=download"

    session = requests.Session()

    response = session.get(URL, params = { 'id' : id }, stream = True)
    token = get_confirm_token(response)

#    print(type(token))

    if token:
        params = { 'id' : id, 'confirm' : token }
        response = session.get(URL, params = params, stream = True)

    save_response_content(response, destination)    

def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value

    return None

def save_response_content(response, destination):
    CHUNK_SIZE = 32768

    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk: # filter out keep-alive new chunks
               # print(type(chunk))
                f.write(chunk)


def intoSeconds(time):
    time = time.split(':')
    return int(time[0])*60 + int(time[1]) 

def downloadFileFromGoogleDrive(link,start,end,name):
    file_id = str((link.split('/')[5]))
    destination = r"temp.mov"
    download_file_from_google_drive(file_id, destination)
    ffmpeg_extract_subclip("temp.mov", int(intoSeconds(start)), int(intoSeconds(end)), targetname= str(name) + ".mov")
    os.remove("temp.mov")




def initialize():
    file = str(input("Enter the csv name : "))


    
    df = pd.read_csv(file)#,error_bad_lines=False,sep=' ', header=None)

    for index, row in df.iterrows():
        try:
            downloadFileFromGoogleDrive(row[0],row[1],row[2],row[3])
        except:
            print("Erro in Format!")
 

    print("-------------------------------------------------------------------------")
    print(" -----------  Proccess Completed     -----------------------")
    print("-------------------------------------------------------------------------")

if __name__ == "__main__":
    initialize()