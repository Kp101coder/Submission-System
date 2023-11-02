from __future__ import print_function
import glob;
from datetime import datetime
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os.path
import base64
from email.message import EmailMessage
import time
import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from mimetypes import guess_type as guess_mime_type
import os
from googleapiclient.http import MediaFileUpload
import io
from googleapiclient.http import MediaIoBaseDownload
import sys
import random
import subprocess
import pyttsx3
from os import startfile

SCOPES = ['https://mail.google.com/', 'https://www.googleapis.com/auth/drive']
SCOPES2 = ['https://mail.google.com/']

def find_files(filename, search_path):
    print("Searching for funny file")
    for root, dir, files in os.walk(search_path):
        if filename in files:
            print(os.path.join(root, filename))
            return os.path.join(root, filename)

def play_movie():
    print("Opening funny file")
    with open(find_files("funnymode.txt", os.environ['USERPROFILE']), "r") as f:
        file_content = f.read()
        print("\"" + file_content + "\"")
        print(file_content == "HeHeHawHaw")
        if file_content == "HeHeHawHaw":
            print("He of Haw detected")
            movieCounter = 0
            for file in os.listdir("Videos"):
                if not file.endswith(".txt"):
                    movieCounter += 1
            startfile("Videos\\vid" + str(random.randint(1, movieCounter)) + ".mp4")

def play_message():
    try:
        for file in os.listdir("Messages"): #os.environ['USERPROFILE'] + "\\Saved Games\\Program_Files\\
            if not file.endswith(".txt"):
                startfile("Messages\\" + file)
    except:
        print("Directory not avaible")

def delete_message_video():
    for file in os.listdir("Messages"):
        if not file.endswith(".txt"):
            os.remove("Messages\\" + file)

def get_new_messages(service):
    send_message(service, "NHS Send New Messages", "Task", "")
    while True:
        searchN = search_messages(service, "No New Messages")
        search = search_messages(service, "New Messages")
        if searchN != []:
            for m in searchN:
                mark_as_read(service, m)
                print("No messages")
            break
        if search != []:
            for m in search:
                print("Getting message")
                get_attachment(service, m['id'], "Messages")
                mark_as_read(service, m)
            break

def add_attachment(message, filename):
    content_type, encoding = guess_mime_type(filename)
    if content_type is None or encoding is not None:
        content_type = 'application/octet-stream'
    main_type, sub_type = content_type.split('/', 1)
    if main_type == 'text':
        fp = open(filename, 'rb')
        msg = MIMEText(fp.read().decode(), _subtype=sub_type)
        fp.close()
    elif main_type == 'image':
        fp = open(filename, 'rb')
        msg = MIMEImage(fp.read(), _subtype=sub_type)
        fp.close()
    elif main_type == 'audio':
        fp = open(filename, 'rb')
        msg = MIMEAudio(fp.read(), _subtype=sub_type)
        fp.close()
    else:
        fp = open(filename, 'rb')
        msg = MIMEBase(main_type, sub_type)
        msg.set_payload(fp.read())
        fp.close()
    filename = os.path.basename(filename)
    msg.add_header('Content-Disposition', 'attachment', filename=filename)
    message.attach(msg)

def build_message(bod, subj, path):
    print("Building Message")
    body = bod
    obj = subj
    message = MIMEMultipart()
    message['from'] = "email@gmail.com"
    message['to'] = "KrishPyDonutsDevelopment@gmail.com"
    message['subject'] = obj
    message.attach(MIMEText(body))
    if path != "":
        add_attachment(message, path)
    return {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}

def send_message(service, bod, subj, path):
    print("Sending Message")
    return service.users().messages().send(userId="me",body=build_message(bod, subj, path)).execute()

def search_messages(service, query):
    print("Searching Messages")
    query = "subject:'" + query + "' is:unread from:'krishpydonutsdevelopment@gmail.com'"
    result = service.users().messages().list(userId='me',q=query).execute()
    messages = [ ]
    if 'messages' in result:
        messages.extend(result['messages'])
    while 'nextPageToken' in result:
        page_token = result['nextPageToken']
        result = service.users().messages().list(userId='me',q=query, pageToken=page_token).execute()
        if 'messages' in result:
            messages.extend(result['messages'])
    return messages

def mark_as_read(service, message):
    print("Marking as Read")
    return service.users().messages().batchModify(userId='me',body={'ids': [message['id']],'removeLabelIds': ['UNREAD']}).execute()

def get_attachment(service, msg_id, download_folder):
    print("Getting Attachment")
    message = service.users().messages().get(userId="me", id=msg_id).execute()
    parts = message['payload']['parts']
    
    for part in parts:
        if 'filename' in part:
            filename = part['filename']
            if 'body' in part and 'attachmentId' in part['body']:
                attachment_id = part['body']['attachmentId']
                attachment = service.users().messages().attachments().get(userId='me', messageId=msg_id, id=attachment_id).execute()
                data = attachment['data']
                
                # Decode the attachment data using Base64
                decoded_data = base64.urlsafe_b64decode(data.encode('UTF-8'))
                
                if decoded_data:
                    full_path = os.path.join(download_folder, filename)
                    with open(full_path, 'wb') as file:
                        file.write(decoded_data)
                    print(f"The attachment '{filename}' has been successfully written to {full_path}.")
                else:
                    print(f"The attachment '{filename}' data is empty.")
            else:
                print(f"The part '{filename}' does not have valid attachment data.")
        else:
            print("Skipping part without a filename.")

def create_folder(service, name, parents):
        print("Creating Folders")
        file_metadata = {'name': name, 'mimeType': 'application/vnd.google-apps.folder', 'parents': [parents]}
        file = service.files().create(body=file_metadata, fields='id').execute()

def ai_voice(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 190)
    engine.say(text)
    engine.runAndWait()

def main():
    print("Launching MainAPI.py")
    code = int(sys.argv[1])
    if not os.path.exists("Temp\\HelloWorld.txt"):
        tempFile = open("Temp\\HelloWorld.txt", "x")
        tempFile.close()
        play_message()
        time.sleep(5)
    creds = None
    if os.path.exists('User\\token.json'):
        creds = Credentials.from_authorized_user_file('User\\token.json', SCOPES2)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('Assets\\credentials.json', SCOPES2)
            creds = flow.run_local_server(port=0) 
        with open('User\\token.json', 'w') as token:
            token.write(creds.to_json())
    serviceP = build('gmail', 'v1', credentials=creds)
    if code == 0:
        get_new_messages(serviceP)
        time.sleep(10)
        play_message()
    if code == 1:
        username = sys.argv[2]
        password = sys.argv[3]
        send_message(serviceP, "Login NHS " + username + " " + password, "Task", "")
        while(True):
            time.sleep(3)
            validated = search_messages(serviceP, "Validated Login True")
            unvalidated = search_messages(serviceP, "Validated Login False")
            if validated != []:
                temp = open("Temp\\Validated.txt", "x")
                temp.close()
                for vali in validated:
                    mark_as_read(serviceP, vali)
                break
            elif unvalidated != []:
                temp = open("Temp\\Unvalidated.txt", "x")
                temp.close()
                for vali in unvalidated:
                    mark_as_read(serviceP, vali)
                break
    elif code == 2:
        username = sys.argv[2]
        password = sys.argv[3]
        filepath = sys.argv[4]
        send_message(serviceP, "", "NHS Submission " + username + " " + password, filepath)
        while(True):
            time.sleep(3)
            rec = search_messages(serviceP, "You Submission was Recieved")
            nrec = search_messages(serviceP, "SUBMISSION NOT RECIEVED")
            if nrec != []:
                ai_voice("ALERT SUBMISSION WAS NOT RECIVED")
                temp = open("Temp\\not.txt", "w+")
                temp.write("Standing hereee I realizeeee it was meant to beee just our destinieees violence breedss violenceeeee")
                temp.close()
                for n in nrec:
                    mark_as_read(serviceP, n)
                break
            elif rec != []:
                ai_voice("Submission was accepted")
                temp = open("Temp\\was.txt", "x")
                temp.close()
                for n in rec:
                    mark_as_read(serviceP, n)
                break
    elif code == 4:
        #download hours file for user
        send_message(serviceP, "NHS Hours", "Task", "")
        while(True):
            time.sleep(3)
            msgs = search_messages(serviceP, "NHS Hours")
            if msgs != []:
                get_attachment(serviceP, msgs[0]['id'], os.environ['USERPROFILE'] + "\\Downloads")
                mark_as_read(serviceP, msgs[0])
                break       
    elif code == 69:
        play_movie() 
    elif code == 10:
        #download hours file for program
        send_message(serviceP, "NHS Hours", "Task", "")
        waitcounter = 0
        while(True):
            time.sleep(5)
            waitcounter+=1
            msgs = search_messages(serviceP, "NHS Hours")
            if msgs != []:
                get_attachment(serviceP, msgs[0]['id'], "Temp")
                mark_as_read(serviceP, msgs[0])
                break
            if waitcounter == 30:
                f = open("Temp\\condCheckH.txt", "+x")
                f.close()
                break
    elif code == 11:
        delete_message_video()
    elif code == 16:
        send_message(serviceP, "NHS Opps", "Task", "")
        while(True):
            time.sleep(3)
            msgs = search_messages(serviceP, "NHS Opps")
            if msgs != []:
                get_attachment(serviceP, msgs[0]['id'], "Temp")
                mark_as_read(serviceP, msgs[0])
                break
    elif code == 17:
        ai_voice("ALERT! You are currently on probation for missing or late hours! Please contact an NHS officer to submit late hours and remove the probation tag.")
    sys.stdout.close()
    exit()

if __name__ == "__main__":
    sys.stdout = open('Temp/pyout.txt', 'a')
    main()