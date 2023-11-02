from __future__ import print_function
from datetime import datetime
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os.path
import base64
from email.message import EmailMessage
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
import openai
from threading import Thread
from pygame import mixer
import time
import random
import threading
from email import encoders

openai.api_key = "null"

SCOPES = ['https://mail.google.com/', 'https://www.googleapis.com/auth/drive']

#Holy shit I need to start fucking documenting my code I cant remeber wtf half of this does
#could have just set the print statments to save to a file...
def upload_log(service, countnum, logid):
    #This function uploads the log file for the server to the folder in the google drive account
    global f
    print("Log Uploaded")
    x = datetime.now().strftime('%m-%d-%Y %I:%M %p')
    performProbationScan(service, x)
    if (int(x[x.index(" ")+1:x.index(" ")+3]) == 10) and x[x.rindex(" ")+1:x.rindex(" ")+3] == "PM":
        f.write("System shutting down for the night...\nHour: " + x[x.index(" ")+1:x.index(" ")+3] + " " + x[x.rindex(" ")+1:x.rindex(" ")+2])
        f.close()
        file_metadata = {'name': filepath, 'mimeType': 'text/plain', 'parents': [logid]}
        media = MediaFileUpload(filepath,mimetype='text/plain')
        service.files().create(body=file_metadata, media_body=media,fields='id').execute()
        time.sleep(5)
        os.system("sudo shutdown --poweroff")
    else:
        f.write("Log Updated: " + str(countnum) + " at " + x + "\n")
        print("Log Updated: " + str(countnum) + " at " + x )
        f.close()
        file_metadata = {'name': filepath, 'mimeType': 'text/plain', 'parents': [logid]}
        media = MediaFileUpload(filepath,mimetype='text/plain')
        service.files().create(body=file_metadata, media_body=media,fields='id').execute() 
        time.sleep(5)
        f = open(filepath,"a+")
        
def search_for_logging_folder(service):
    #This method searches for the folder that stores all
    print("Searching for Server Folder")
    files = []
    page_token = None
    while True:
        response = service.files().list(q="mimeType='application/vnd.google-apps.folder' and name contains 'Server Logging' and trashed=false", spaces='drive', fields='nextPageToken, ''files(id, name)',pageToken=page_token).execute()
        files.extend(response.get('files', []))
        page_token = response.get('nextPageToken', None)
        if page_token is None:
            break
    return files[0].get('id')

def performProbationScan(service, date):
    global dateChecker
    global dateCheckerMao
    if dateChecker == "":
        f.write("\tPerforming Daily Scan NHS\n")
        print("Performing Daily Scan NHS")
        download_file(service, search_for_file(service, "dueDate.txt", "text/plain", search_for_file(service, "NHS", "application/vnd.google-apps.folder", None)), "dueDate.txt")
        reader = open("dueDate.txt", "r")
        fileContents = reader.read()
        fileContents = fileContents.split(" ")
        dateOnFile = fileContents[0]  
        reqTotal = int(fileContents[1])
        reqClub = int(fileContents[2])
        reader.close()
        os.remove("dueDate.txt")
        if dateOnFile in date:
            f.write("\tDue date registerd, checking hours\n")
            print("Due date registered, checking hours")
            download_file(service, search_for_file(service, "studentHours.txt", "text/plain", search_for_file(service, "NHS", "application/vnd.google-apps.folder", None)), "studentHours.txt")
            data = []
            with open("studentHours.txt", "r") as reader:
                for line in reader:
                    if ":" in line:
                        data.append(line.strip())
            reader = open("studentHours.txt", "w")
            indexCount = 0
            probCount = 0
            for userProfile in data:
                print("Line: \"" + str(userProfile) + "\"")
                indexCount+=1
                profile = userProfile.split("\t")
                clubHours = 0
                totalHours = 0
                for profileData in profile:
                    if "Club:" in profileData:
                        clubHours = float(profileData[profileData.find(":") + 1:])
                    if "Accepted:" in profileData:
                        totalHours = float(profileData[profileData.find(":") + 1:])
                if clubHours < reqClub or totalHours < reqTotal:
                    probCount+=1
                    for profileData in profile:
                        if "Probation:" not in profileData:
                            reader.write(profileData+"\t")
                        else:
                            reader.write("Probation:true")
                else:
                    reader.write(userProfile)
                if indexCount != len(data):
                    reader.write("\n")
            reader.close()
            try:
                delete_file(service, search_for_file(service, "studentHours.txt", "text/plain", search_for_file(service, "NHS", "application/vnd.google-apps.folder", None)))
            except:
                ...
            upload_file(service, "studentHours.txt", search_for_file(service, "NHS", "application/vnd.google-apps.folder", None), "text/plain")
            f.write("\tProhibited NHS Studets: " + str(probCount) + "\n")
            print("Prohibited NHS Studets: " + str(probCount))
            os.remove("studentHours.txt")
        dateChecker = date[0:10]
    elif dateChecker not in date:
        dateChecker = ""
    if dateCheckerMao == "":
        f.write("\tPerforming Daily Scan MAO\n")
        print("Performing Daily Scan MAO")
        download_file(service, search_for_file(service, "dueDate.txt", "text/plain", search_for_file(service, "MAO", "application/vnd.google-apps.folder", None)), "dueDate.txt")
        reader = open("dueDate.txt", "r")
        fileContents = reader.read()
        fileContents = fileContents.split(" ")
        dateOnFile = fileContents[0]  
        reqTotal = int(fileContents[1])
        reqClub = int(fileContents[2])
        reader.close()
        os.remove("dueDate.txt")
        if dateOnFile in date:
            f.write("\tDue date registerd, checking hours\n")
            print("Due date registered, checking hours")
            download_file(service, search_for_file(service, "studentHours.txt", "text/plain", search_for_file(service, "MAO", "application/vnd.google-apps.folder", None)), "studentHours.txt")
            data = []
            with open("studentHours.txt", "r", encoding="utf-8") as reader:
                for line in reader:
                    if ":" in line:
                        data.append(line.strip())
            reader = open("studentHours.txt", "w")
            indexCount = 0
            probCount = 0
            for userProfile in data:
                indexCount+=1
                profile = userProfile.split("\t")
                clubHours = 0
                totalHours = 0
                for profileData in profile:
                    if "Club:" in profileData:
                        clubHours = float(profileData[profileData.find(":") + 1:])
                    if "Accepted:" in profileData:
                        totalHours = float(profileData[profileData.find(":") + 1:])
                if clubHours < reqClub or totalHours < reqTotal:
                    probCount+=1
                    for profileData in profile:
                        if "Probation:" not in profileData:
                            reader.write(profileData+"\t")
                        else:
                            reader.write("Probation:true")
                else:
                    reader.write(userProfile)
                if indexCount != len(data):
                    reader.write("\n")
            reader.close()
            try:
                delete_file(service, search_for_file(service, "studentHours.txt", "text/plain", search_for_file(service, "MAO", "application/vnd.google-apps.folder", None)))
            except:
                ...
            upload_file(service, "studentHours.txt", search_for_file(service, "MAO", "application/vnd.google-apps.folder", None), "text/plain")
            f.write("\tProhibited MAO Studets: " + str(probCount) + "\n")
            print("Prohibited MAO Studets: " + str(probCount))
            os.remove("studentHours.txt")
        dateCheckerMao = date[0:10]
    elif dateCheckerMao not in date:
        dateCheckerMao = ""

def search_for_log_files(service):
    files = []
    page_token = None
    while True:
        response = service.files().list(q="mimeType='text/plain' and name contains '" + str(counter) + "' and trashed=false and parents in '" + search_for_logging_folder(service) + "'", spaces='drive', fields='nextPageToken, ''files(id, name)',pageToken=page_token).execute()
        files.extend(response.get('files', []))
        page_token = response.get('nextPageToken', None)
        if page_token is None:
            break
    return files[0].get('id')

def delete_file(service, file_id):
    service.files().delete(fileId=file_id).execute()

def create_and_save_log(service):
    global counter
    global dateChecker
    global dateCheckerMao
    dateChecker = ""
    dateCheckerMao = ""
    counter = 0
    page_token = None
    response = service.files().list(q="mimeType='text/plain' and name contains 'System' and parents in '" + search_for_logging_folder(service) + "' and trashed=false",spaces='drive',fields='nextPageToken, ''files(id, name)', pageToken=page_token).execute()
    for file in response.get('files', []):
        counter+=1
    global filepath
    filepath  = "System Log" + str(counter) + ".txt"
    print("File path = " + filepath)
    global f
    try:
        os.remove("System Log" + str(counter-2) + ".txt")
        print("File before previous deleted.")
    except:
        print("File before previous non-existent.")
    f = open(filepath,"w+")
    f.write("Program started\n")
    f.write("Log Created\n")
    print("Log Created")

def add_attachment(message, filename):
    f.write("\t\t\t\tAdding Attachment\n")
    print("\t\t\t\tAdding Attachment")
    content_type, encoding = guess_mime_type(filename)
    print("\t\t\t\t\t" + filename + str(guess_mime_type(filename)))
    f.write("\t\t\t\t\t" + filename + str(guess_mime_type(filename)) + "\n")
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
    elif main_type == 'video':  # Add this case for videos
        msg = MIMEBase('application', 'octet-stream')
        msg.set_payload(open(filename, 'rb').read())
        encoders.encode_base64(msg)
    else:
        fp = open(filename, 'rb')
        msg = MIMEBase(main_type, sub_type)
        msg.set_payload(fp.read())
        fp.close()
    filename = os.path.basename(filename)
    msg.add_header('Content-Disposition', 'attachment', filename=filename)
    message.attach(msg)

#Fuck me why didnt I just make one general one instead of a bunch of the fucking same thing with slight differences
def build_message_token(destination):
    print("\t\t\t\tBuilding Message Token")
    f.write("\t\t\t\tBuilding Message Token\n")
    body = "Please do not delete this message or manipulate it in any way.\nThis is your authentication token and once you run your software it will automatically be applied and you may delete it if you wish.\nKrishPy Donuts Development"
    obj = "Authentication Token Refresh"
    message = MIMEMultipart()
    message['to'] = destination
    message['from'] = "KrishPyDonutsDevelopment@gmail.com"
    message['subject'] = obj
    message.attach(MIMEText(body))
    add_attachment(message, "token.json")
    return {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}

def build_message(destination, subject, bod, attach):
    print("\t\t\t\tBuilding Message")
    f.write("\t\t\t\tBuilding Message\n")
    message = MIMEMultipart()
    message['to'] = destination
    message['from'] = "KrishPyDonutsDevelopment@gmail.com"
    message['subject'] = subject
    message.attach(MIMEText(bod))
    if attach != "":
        add_attachment(message, attach)
    return {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}

def build_message_submission(destination):
    print("\t\t\t\tBuilding Message Submission")
    f.write("\t\t\t\tBuilding Message Submission\n")
    body = "No Take Backsies! I hope you checked what image you sent BEFORE you submit!"
    obj = "You Submission was Recieved"
    message = MIMEMultipart()
    message['to'] = destination
    message['from'] = "KrishPyDonutsDevelopment@gmail.com"
    message['subject'] = obj
    message.attach(MIMEText(body))
    return {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}

def build_message_submission_fail(destination, error):
    print("\t\t\t\tBuilding Message Submission Fail")
    f.write("\t\t\t\tBuilding Message Submission Fail\n")
    body = "If this is your first Submission... USE THE SOFTWARE FIRST!!! (Yes I want you to download it, it's cool and I worked hard on it)\nDonwload link: https://krishpyddev.com/software-download/\nMake sure you followed the correct Submission format as it was declined!\nThis is how you are supposed to do it:\nSubject: \"NHS(space)userid(space)password\"\nObviously replace space with an actual space, and the email should have your picture attachment, AND replace NHS with MAO if you are submitting for MAO!\nAlso if you are submitting for MAO, include a note in the body if needed.\nError Message: "+ error
    obj = "SUBMISSION NOT RECIEVED"
    message = MIMEMultipart()
    message['to'] = destination
    message['from'] = "KrishPyDonutsDevelopment@gmail.com"
    message['subject'] = obj
    message.attach(MIMEText(body))
    return {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}

def build_message_ai(destination, answer, question):
    print("\t\t\t\tBuilding Message from AI")
    f.write("\t\t\t\tBuilding Message from AI\n")
    body = "*Note: If you are trying to submit a form, the email should look like this...\nSubject: \"Submission(space)userid(space)password\"\nObviously replace space with an actual space, and the email should have your picture attachment!\n\nQuestion:\n" + question + "\n\nAnswer:\n" + answer
    obj = "Sending me an email huh? Ask me any question (in the email body), I'll give you an answer."
    message = MIMEMultipart()
    message['to'] = destination
    message['from'] = "KrishPyDonutsDevelopment@gmail.com"
    message['subject'] = obj
    message.attach(MIMEText(body))
    return {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}

def send_message_token(service, destination):
    print("\t\t\t\tSending Message Token")
    f.write("\t\t\t\tSending Message Token\n")
    return service.users().messages().send(userId="me",body=build_message_token(destination)).execute()

def send_message(service, destination, subject, bod, attach):
    print("\t\t\t\tSending Message")
    f.write("\t\t\t\tSending Message\n")
    if random.randint(1,100) == 69:
        print("\t\t\t\t\tLUCKY WINNER")
        f.write("\t\t\t\t\tLUCKY WINNER\n")
        txt = (
        "Jk                                            \n"
        "⠀⠀⠀⢰⠶⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⠶⠲⣄⠀\n"
        "⠀⠀⣠⡟⠀⠈⠙⢦⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⡶⣦⣀⠀⠀⠀⠀⠀⠀⠀⠀⣠⠾⠋⠁⠀⠀⢽⡄\n"
        "⠀⠀⡿⠀⠀⠀⠀⠀⠉⠷⣄⣀⣤⠤⠤⠤⠤⢤⣷⡀⠙⢷⡄⠀⠀⠀⠀⣠⠞⠉⠀⠀⠀⠀⠀⠈⡇\n"
        "⠀⢰⡇⠀⠀⠀⠀⠀⠀⠀⠉⠳⣄⠀⠀⠀⠀⠀⠈⠁⠀⠀⠹⣦⠀⣠⡞⠁⠀⠀⠀⠀⠀⠀⠀⠀⡗\n"
        "⠀⣾⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣻⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣏\n"
        "⠀⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⡇\n"
        "⠀⡿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⠂\n"
        "⠀⢿⠀⠀⠀⠀⣤⣤⣤⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣤⣤⣤⣤⣤⡀⠀⠀⠀⠀⠀⣸⠇⠀\n"
        "⠀⠘⣇⠀⠀⠀⠀⠉⠉⠛⠛⢿⣶⣦⠀⠀⠀⠀⠀⠀⢴⣾⣟⣛⡋⠋⠉⠉⠁⠀⠀⠀⠀⣴⠏⠀⠀\n"
        "⢀⣀⠙⢷⡄⠀⠀⣀⣤⣶⣾⠿⠋⠁⠀⢴⠶⠶⠄⠀⠀⠉⠙⠻⠿⣿⣷⣶⡄⠀⠀⡴⠾⠛⠛⣹⠇\n"
        "⢸⡍⠉⠉⠉⠀⠀⠈⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ ⠀⠀⠀⠀⣬⠷⣆⣠⡤⠄⢀⣤⠞⠁⠀\n"
        "⠈⠻⣆⡀⠶⢻⣇⡴⠖⠀⠀⠀⣴⡀⣀⡴⠚⠳⠦⣤⣤⠾⠀⠀⠀⠀⠀⠘⠟⠋⠀⠀⠀⢻⣄⠀⠀\n"
        "⠀⠀⣼⠃⠀⠀⠉⠁⠀⠀⠀⠀⠈⠉⢻⡆⠀⠀⠀⠀⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⠀⠀\n"
        "⠀⢠⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⡀⠀⠀ ⢀⡇⠀   ⠀⠀⠀⣀⡿⠧⠿⠿⠟⠀⠀\n"
        "⠀⣾⡴⠖⠛⠳⢦⣿⣶⣄⣀⠀⠀⠀⠀⠘⢷⣀⠀⣸⠃⠀⠀⠀⣀⣀⣤⠶⠚⠉⠀⠀⠀⠀⠀⠀⠀\n"
        "⠀⠀⠀⠀⠀⠀⠀⠈⢷⡀⠈⠻⠦⠀⠀⠀⠀⠉⠉⠁⠀⠀⠀⠀⠹⣆⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n"
        "⠀⠀⠀⠀⠀⠀⠀⢀⡴⠟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢳⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀\n"
        "⠀⠀⠀⠀⠀⠀⢠⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠻⡄⠀⠀⠀⠀⠀⠀⠀⠀\n"
        "⠀⠀⠀⠀⠀⠀⠈⠉⠛⠛⢲⡗⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⡆⠀⠀⠀⠀⠀⠀⠀\n"
        "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡇⠀⠀⠀⠀⠀⠀⠀\n"
        "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠋⠀⠀⠀⠀⠀⠀⠀\n"
        "Haha now you die of cringe                    "
        )
        service.users().messages().send(userId="me",body=build_message(destination, "Congratulations 1%%er! You won the lottery!", txt, "")).execute()
    return service.users().messages().send(userId="me",body=build_message(destination, subject, bod, attach)).execute()

def send_message_ai(service, destination, question):
    print("\t\t\t\tSending Message from AI")
    f.write("\t\t\t\tSending Message from AI\n")
    return service.users().messages().send(userId="me",body=build_message_ai(destination, chatGPT(question), question)).execute()

def search_messages_token(service):
    print("\t\tSearching Messages Requesting")
    f.write("\t\tSearching Messages Requesting\n")
    query = "subject:'Token Refresh Request | Code: KPDD710' and is:unread"
    result = service.users().messages().list(userId='me',q=query).execute()
    messages = []
    if 'messages' in result:
        messages.extend(result['messages'])
    while 'nextPageToken' in result:
        page_token = result['nextPageToken']
        result = service.users().messages().list(userId='me',q=query, pageToken=page_token).execute()
        if 'messages' in result:
            messages.extend(result['messages'])
    return messages

def find_From(service, message):
    print("\t\t\t\tFinding From Address")
    f.write("\t\t\t\tFinding From Address\n")
    msg = service.users().messages().get(userId='me', id=message['id'], format='full').execute()
    payload = msg['payload']
    headers = payload.get("headers")
    parts = payload.get("parts")
    folder_name = "email"
    has_subject = False
    value = ""
    if headers:
        for header in headers:
            name = header.get("name")
            value = header.get("value")
            if name.lower() == 'from':
                try:
                    value=value[value.index('<')+1:value.index('>')]
                    break
                except:
                    break
    if "prabhukrish710@gmail.com" in value:
        return value
    else:
        if(int(emails.get(value, 0)) > 20):
            print("\t\tMessage OverFrequency: Sending FAIL Data to " + value)
            f.write("\t\tMessage OverFrequency: Sending FAIL Data to " + value + "\n")
            send_Message_Submission_Fail(service, value, "Error, this email has sent too many requests today. Please try again tommorow.")
            mark_as_read(service, message)
            f.write("\t\tEmails Dictionary: " + str(emails) + "\n")
            print("\t\tEmails Dictionary: " + str(emails))
            raise Exception("OverFrequency Error")
        else:
            emails.update({value: int(emails.get(value, 0))+1})
            return value

def find_Bod(service, message):
    print("\t\t\t\tFinding Body")
    f.write("\t\t\t\tFinding Body\n")
    msg = service.users().messages().get(userId='me', id=message['id'], format='full').execute()
    if msg.get("payload").get("body").get("data"):
        return base64.urlsafe_b64decode(msg.get("payload").get("body").get("data").encode("ASCII")).decode("utf-8")
    return msg.get("snippet") 

def find_subject(service, msg):
    print("\t\t\t\tFinding Subject")
    f.write("\t\t\t\tFinding Subject\n")
    message = service.users().messages().get(userId="me", id=msg['id'], format='full').execute()
    for header in message['payload']['headers']:
        if header['name'] == 'Subject':
            subject = header['value']
            break
    if '=?' in subject:
        subject = ''.join(base64.b64decode(subject.split('?')[3]).decode())
    return subject

def mark_as_read(service, message):
    print("\t\t\t\tMarking as Read")
    f.write("\t\t\t\tMarking as Read\n")
    return service.users().messages().batchModify(userId='me',body={'ids': [message['id']],'removeLabelIds': ['UNREAD']}).execute()

def searching_Inc_Messages(service):
    print("\t\tSearching AI Messages")
    f.write("\t\tSearching AI Messages\n")
    query = 'is:unread -subject:"Submission" -subject"Token" -subject:"Task"' 
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

def searching_submissions(service, club):
    print("\t\tSearching Submission Messages " + club)
    f.write("\t\tSearching Submission Messages " + club + "\n")
    query = "subject:'" + club + " ' is:unread"
    result = service.users().messages().list(userId='me',q=query).execute()
    messages = []
    if 'messages' in result:
        messages.extend(result['messages'])
    while 'nextPageToken' in result:
        page_token = result['nextPageToken']
        result = service.users().messages().list(userId='me',q=query, pageToken=page_token).execute()
        if 'messages' in result:
            messages.extend(result['messages'])
    return messages

def send_Message_Submission(service, destination):
    print("\t\t\t\tSending Submission Acceptance")
    f.write("\t\t\t\tSending Submission Acceptance\n")
    return service.users().messages().send(userId="me",body=build_message_submission(destination)).execute()

def send_Message_Submission_Fail(service, destination, error):
    print("\t\t\t\tSending Submission Fail")
    f.write("\t\t\t\tSending Submission Fail\n")
    return service.users().messages().send(userId="me",body=build_message_submission_fail(destination, error)).execute()

def download_file(service, file_id, filepath):
    print("\t\t\t\tDownloading File")
    f.write("\t\t\t\tDownloading File\n")
    file = service.files().get_media(fileId=file_id).execute()
    # Write the content to a file
    with io.open(filepath, "w", encoding="utf-8") as j:
        for character in file.decode("utf-8"):
            if not character == "\n":
                j.write(character)

def check_user(user, pswrd, ch):
    print("\t\t\t\tChecking User")
    f.write("\t\t\t\tChecking User\n")
    #checks to see if the suer credentials are correct
    #if ch = true it will return true or false. Otherwise it will return the useres grade if the user exists or false if their login is wrong
    datafile = open("userLoginValues.txt", "r")
    data = datafile.read()
    data = data.split("\n")
    for val in data:
        u = val.split(":")
        if u[0] == user and u[1] == pswrd:
            if ch:
                return True
            else:
                return u[2]
    return False

def search_for_file(service, name, type, parents):
    print("\t\t\t\tSearching for File")
    f.write("\t\t\t\tSearching for File\n")
    #application/vnd.google-apps.folder
    #text/plain
    files = []
    page_token = None
    while True:
        if parents != None:
            response = service.files().list(q="mimeType='" + type + "' and name contains '" + name + "' and parents in '" + parents + "' and trashed=false", spaces='drive', fields='nextPageToken, ''files(id, name)',pageToken=page_token).execute()
        elif name == None:
            response = service.files().list(q="mimeType='" + type + "' and parents in '" + parents + "' and trashed=false", spaces='drive', fields='nextPageToken, ''files(id, name)',pageToken=page_token).execute()
        else:
            response = service.files().list(q="mimeType='" + type + "' and name contains '" + name + "' and trashed=false", spaces='drive', fields='nextPageToken, ''files(id, name)',pageToken=page_token).execute()
        files.extend(response.get('files', []))
        page_token = response.get('nextPageToken', None)
        if page_token is None:
            break
    return files[0].get('id')

def get_attachment(service, msg_id):
    print("\t\t\t\tGetting Attachment")
    f.write("\t\t\t\tGetting Attachment\n")
    message = service.users().messages().get(userId="me", id=msg_id).execute()
    parts = message['payload']['parts']
    file_path = ""
    # Iterate through the parts of the email message
    for part in parts:
        # Check if the part has the 'body' field
        if part['filename'].endswith('.jpeg') or part['filename'].endswith('.jpg') or part['filename'].endswith('.JPG') or part['filename'].endswith('.JPEG'):
            if 'body' in part:
                # Get the attachment ID
                attachment_id = part['body']['attachmentId']
                # Fetch the attachment using its ID
                attachment = service.users().messages().attachments().get(userId='me', messageId=msg_id, id=attachment_id).execute()
                # Decode the attachment data
                data = attachment['data']
                file_data = base64.urlsafe_b64decode(data.encode('UTF-8'))
                if file_data:
                    # Write the decoded data to a file
                    file_path = part['filename']
                    with open(file_path, 'wb') as j:
                        j.write(file_data)
                    j.close()
                    print(f"\t\t\t\tThe attachment has been successfully written to {file_path}.")
                else:
                    print("\t\t\t\tThe attachment data is empty.")
            else:
                print("\t\t\t\tThe part does not have a 'body' field.")
    return file_path

def upload_file(service, filepathtoupload, parents, type):
    print("\t\t\t\tFile uploaded")
    f.write("\t\t\t\tFile uploaded\n")
    file_metadata = {'name': filepathtoupload, 'parents': [parents]}
    media = MediaFileUpload(filepathtoupload,mimetype=type)
    service.files().create(body=file_metadata, media_body=media,fields='id').execute() 

def upload_submission(service, serviceD, msid, parents):
    print("\t\t\t\tUploading submission")
    f.write("\t\t\t\tUploading submission\n")
    filepathing = get_attachment(service, msid)
    if filepathing == "":
        raise Exception("Must be a .jpeg or .jpg file! Use a file converter to change to .jpeg\nRecomended Converter: https://image.online-convert.com/convert-to-jpg")
    upload_file(serviceD, filepathing, parents, "image/jpeg")
    return filepathing

def searching_MAO(service):
    print("\t\tSearching MAO Messages")
    f.write("\t\tSearching MAO Messages\n")
    query = "subject:'MAO' is:unread"
    result = service.users().messages().list(userId='me',q=query).execute()
    messages = []
    if 'messages' in result:
        messages.extend(result['messages'])
    while 'nextPageToken' in result:
        page_token = result['nextPageToken']
        result = service.users().messages().list(userId='me',q=query, pageToken=page_token).execute()
        if 'messages' in result:
            messages.extend(result['messages'])
    return messages

def chatGPT(question):
    try:
        if len(question) > 200:
            raise Exception("Over 200 character limit. Pay me money if you want more. OpenAI ain't cheap.")
        print("\t\t\t\tAsking Question")
        f.write("\t\t\t\tAsking Question\n")
        
        #Code Generated by ChatGPT

        # Let's now create a function that takes in a question as input and returns the answer
        response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=question,
                max_tokens=1024
            )
        answer=response["choices"][0]["text"]
        print("\t\t\t\tQuestion: " + question)
        f.write("\t\t\t\tQuestion: " + question + "\n")
        print("\t\t\t\tAnswer: " + answer)
        f.write("\t\t\t\tAnswer: " + answer + "\n")
        return answer
    except Exception as e:
        f.write("\t\t\t\t\tTHERE WAS AN ERROR ASKING QUESTION\n\t\t\t\t\t" + str(e) + "\n")
        return "There seems to have been an error. Please try again later."

def search_tasks(service):
    print("\t\tSearching Task Messages")
    f.write("\t\tSearching Task Messages\n")
    query = "subject:'Task' is:unread"
    result = service.users().messages().list(userId='me',q=query).execute()
    messages = []
    if 'messages' in result:
        messages.extend(result['messages'])
    while 'nextPageToken' in result:
        page_token = result['nextPageToken']
        result = service.users().messages().list(userId='me',q=query, pageToken=page_token).execute()
        if 'messages' in result:
            messages.extend(result['messages'])
    return messages

def create_folder(service, name, parents):
    print("\t\t\t\tCreating Folder")
    f.write("\t\t\t\tCreating Folder\n")
    file_metadata = {'name': name, 'mimeType': 'application/vnd.google-apps.folder', 'parents': [parents]}
    file = service.files().create(body=file_metadata, fields='id').execute()

def get_new_messages(service, mainParent):
    print("\t\t\t\tGetting new Messages")
    f.write("\t\t\t\tGetting new Messages\n")
    files = []
    page_token = None
    while True:
        response = service.files().list(q="mimeType='video/mp4' and parents in '" + search_for_file(service, "Message", "application/vnd.google-apps.folder", mainParent) + "' and trashed=false", spaces='drive', fields='nextPageToken, ''files(id, name)',pageToken=page_token).execute()
        page_token = response.get('nextPageToken', None)
        files.extend(response.get('files', []))
        page_token = response.get('nextPageToken', None)
        if page_token is None:
            break
    fileslist = []
    for file in files:
        download_video(service, file['id'], file['name'])
        fileslist.append(file['name'])
    return fileslist

def download_video(service, file_id, file_name):
    print("\t\t\t\tDownloading Video")
    f.write("\t\t\t\tDownloading Video\n")
     # Get the file metadata to retrieve the MIME type
    file_metadata = service.files().get(fileId=file_id).execute()

    # Download the file contents
    request = service.files().get_media(fileId=file_id)
    file_content = io.BytesIO()
    downloader = MediaIoBaseDownload(file_content, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print(f"\t\t\t\t\tDownload {int(status.progress() * 100)}%.")

    # Write the downloaded content to a file
    with open(file_name, "wb") as writefile:
        writefile.write(file_content.getbuffer())

def message_function(fromEmail, service, serviceD, NHSID):
    print("\t\t\t\tUploading messages to: " + fromEmail)
    f.write("\t\t\t\tUploading messages to: " + fromEmail + "\n")
    movies = get_new_messages(serviceD, NHSID)
    if movies != []:
        for movie in movies:
            send_message(service, fromEmail, "New Messages", "", movie)
            os.remove(movie)
    else:
        send_message(service, fromEmail, "No New Messages", "", "")

def main():
    print("Launching serverAPI.py")
    mixer.init()
    for i in range(1,7):
        mixer.music.load("serveraudio" + str(i) + ".mp3")
        mixer.music.play()
        while mixer.music.get_busy():  # wait for music to finish playing
            time.sleep(1)
    creds = None
    try:
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
                creds = flow.run_local_server(port=0) 
            with open('token.json', 'w') as token:
                token.write(creds.to_json())
    except:
        os.system("cd Desktop")
        os.system("python serverAPI.py")
        exit()
    serviceD = build('drive', 'v3', credentials=creds)
    service = build('gmail', 'v1', credentials=creds)
    create_and_save_log(serviceD)
    logfolder = search_for_logging_folder(serviceD)
    global emails
    emails = {}
    try:
        create_and_save_log(serviceD)
        counterS = 0
        f.write("Launching serverAPI.py\n")
        updateCount = 0
        errCounter = 0
        cont=True
        contC=True
        #Download api key
        try:
            download_file(serviceD, search_for_file(serviceD, "apikey.txt", "text/plain", None), "apikey.txt")
            apikeyreader = open("apikey.txt", "r")
            openai.api_key = apikeyreader.read()
            chatGPT("Testing")
        except Exception as e:
            txt = (
            "⠀⠀⠀⢰⠶⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⠶⠲⣄⠀\n"
            "⠀⠀⣠⡟⠀⠈⠙⢦⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⡶⣦⣀⠀⠀⠀⠀⠀⠀⠀⠀⣠⠾⠋⠁⠀⠀⢽⡄\n"
            "⠀⠀⡿⠀⠀⠀⠀⠀⠉⠷⣄⣀⣤⠤⠤⠤⠤⢤⣷⡀⠙⢷⡄⠀⠀⠀⠀⣠⠞⠉⠀⠀⠀⠀⠀⠈⡇\n"
            "⠀⢰⡇⠀⠀⠀⠀⠀⠀⠀⠉⠳⣄⠀⠀⠀⠀⠀⠈⠁⠀⠀⠹⣦⠀⣠⡞⠁⠀⠀⠀⠀⠀⠀⠀⠀⡗\n"
            "⠀⣾⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣻⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣏\n"
            "⠀⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⡇\n"
            "⠀⡿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⠂\n"
            "⠀⢿⠀⠀⠀⠀⣤⣤⣤⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣤⣤⣤⣤⣤⡀⠀⠀⠀⠀⠀⣸⠇⠀\n"
            "⠀⠘⣇⠀⠀⠀⠀⠉⠉⠛⠛⢿⣶⣦⠀⠀⠀⠀⠀⠀⢴⣾⣟⣛⡋⠋⠉⠉⠁⠀⠀⠀⠀⣴⠏⠀⠀\n"
            "⢀⣀⠙⢷⡄⠀⠀⣀⣤⣶⣾⠿⠋⠁⠀⢴⠶⠶⠄⠀⠀⠉⠙⠻⠿⣿⣷⣶⡄⠀⠀⡴⠾⠛⠛⣹⠇\n"
            "⢸⡍⠉⠉⠉⠀⠀⠈⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ ⠀⠀⠀⠀⣬⠷⣆⣠⡤⠄⢀⣤⠞⠁⠀\n"
            "⠈⠻⣆⡀⠶⢻⣇⡴⠖⠀⠀⠀⣴⡀⣀⡴⠚⠳⠦⣤⣤⠾⠀⠀⠀⠀⠀⠘⠟⠋⠀⠀⠀⢻⣄⠀⠀\n"
            "⠀⠀⣼⠃⠀⠀⠉⠁⠀⠀⠀⠀⠈⠉⢻⡆⠀⠀⠀⠀⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⠀⠀\n"
            "⠀⢠⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⡀⠀⠀ ⢀⡇⠀   ⠀⠀⠀⣀⡿⠧⠿⠿⠟⠀⠀\n"
            "⠀⣾⡴⠖⠛⠳⢦⣿⣶⣄⣀⠀⠀⠀⠀⠘⢷⣀⠀⣸⠃⠀⠀⠀⣀⣀⣤⠶⠚⠉⠀⠀⠀⠀⠀⠀⠀\n"
            "⠀⠀⠀⠀⠀⠀⠀⠈⢷⡀⠈⠻⠦⠀⠀⠀⠀⠉⠉⠁⠀⠀⠀⠀⠹⣆⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n"
            "⠀⠀⠀⠀⠀⠀⠀⢀⡴⠟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢳⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀\n"
            "⠀⠀⠀⠀⠀⠀⢠⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠻⡄⠀⠀⠀⠀⠀⠀⠀⠀\n"
            "⠀⠀⠀⠀⠀⠀⠈⠉⠛⠛⢲⡗⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⡆⠀⠀⠀⠀⠀⠀⠀\n"
            "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡇⠀⠀⠀⠀⠀⠀⠀\n"
            "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠋⠀⠀⠀⠀⠀⠀⠀\n"
            "Haha now you die of cringe                    "
            )
            send_message(service, "prabhukrish710@gmail.com", "API Key not found :(", txt, "")
        while(True):
            try:
                counterS+=1
                print("\tSearching: " + str(counterS))
                f.write("\tSearching: " + str(counterS) + "\n")
                #token request ONLY
                requests = search_messages_token(service)
                if requests != []:
                    requestsCount = 0
                    for message in requests:
                        print("\t\t\tRequest Found")
                        f.write("\t\t\tRequest Found\n")
                        requestsCount+=1
                        fromEmail = find_From(service, message)
                        print("\t\tMessage " + str(requestsCount) + ": Sending Data to " + fromEmail)
                        f.write("\t\tMessage " + str(requestsCount) + ": Sending Data to " + fromEmail + "\n")
                        send_message_token(service, fromEmail)
                        mark_as_read(service, message)
                #submission
                submissionsNHS = searching_submissions(service , "NHS")
                if submissionsNHS != []:
                    NHSID = search_for_file(serviceD, "NHS", "application/vnd.google-apps.folder", None)
                    try:
                        download_file(serviceD, search_for_file(serviceD, "userLoginValues.txt", "text/plain", NHSID), "userLoginValues.txt")
                        cont = True
                    except:
                        if cont:
                            send_Message_Submission_Fail(service, "prabhukrish710@gmail.com", "The values file is unable to be retrived. Might be getting edits...")
                        cont=False
                    messageCount = 0
                    if cont:
                        for message in submissionsNHS:
                            print("\t\t\tSubmission Found")
                            f.write("\t\t\tSubmission Found\n")
                            messageCount+=1
                            fromEmail = find_From(service, message)
                            subjectLine = find_subject(service, message)
                            try:
                                userID = subjectLine[len("NHS Submission "):subjectLine.rindex(" ")]
                                password = subjectLine[subjectLine.rindex(" ")+1:len(subjectLine)]
                                if check_user(userID, password, True):
                                    ugrade = check_user(userID, password, False)
                                    print("\t\t\t\tUploading info from UserID: " + userID + " and Password: " + password + " and Grade: " + ugrade)
                                    f.write("\t\t\t\tUploading info from UserID: " + userID + " and Password: " + password + " and Grade: " + ugrade + "\n")
                                    gradeID = search_for_file(serviceD, ugrade, "application/vnd.google-apps.folder", NHSID)
                                    try:
                                        studentID = search_for_file(serviceD, userID, "application/vnd.google-apps.folder", gradeID)
                                        unrevID = search_for_file(serviceD, "Unreviewed", "application/vnd.google-apps.folder", studentID)
                                        filepathimg = upload_submission(service, serviceD, message['id'], unrevID)
                                        mark_as_read(service, message)
                                        print("\t\tMessage " + str(messageCount) + ": Sending Data to " + fromEmail)
                                        f.write("\t\tMessage " + str(messageCount) + ": Sending Data to " + fromEmail + "\n")
                                        send_Message_Submission(service, fromEmail)
                                        os.remove(filepathimg)
                                    except:
                                        #create id folder and all subfolders (second api command in student screen)
                                        create_folder(serviceD, userID, gradeID)
                                        studentID = search_for_file(serviceD, userID, "application/vnd.google-apps.folder", gradeID)
                                        create_folder(serviceD, "Unreviewed", studentID)
                                        create_folder(serviceD, "Approved", studentID)
                                        create_folder(serviceD, "Disapproved", studentID)
                                        unrevID = search_for_file(serviceD, "Unreviewed", "application/vnd.google-apps.folder", studentID)
                                        filepathimg = upload_submission(service, serviceD, message['id'], unrevID)
                                        mark_as_read(service, message)
                                        print("\t\tMessage " + str(messageCount) + ": Sending Data to " + fromEmail)
                                        f.write("\t\tMessage " + str(messageCount) + ": Sending Data to " + fromEmail + "\n")
                                        send_Message_Submission(service, fromEmail)
                                        os.remove(filepathimg)
                                else:
                                    raise Exception("Username and Password did not match")
                            except Exception as e:
                                print("\t\tMessage " + str(messageCount) + ": Sending FAIL Data to " + fromEmail)
                                f.write("\t\tMessage " + str(messageCount) + ": Sending FAIL Data to " + fromEmail + "\n")
                                send_Message_Submission_Fail(service, fromEmail, str(e))
                                mark_as_read(service, message)
                        os.remove("userLoginValues.txt")
                submissionsMAO = searching_submissions(service, "MAO")
                if submissionsMAO != []:
                    MAOID = search_for_file(serviceD, "MAO", "application/vnd.google-apps.folder", None)
                    try:
                        download_file(serviceD, search_for_file(serviceD, "userLoginValues.txt", "text/plain", MAOID), "userLoginValues.txt")
                        contC = True
                    except:
                        if contC:
                            send_Message_Submission_Fail(service, "prabhukrish710@gmail.com", "The values file is unable to be retrived. Might be getting edits...")
                        contC=False
                    messageCount = 0
                    if contC:
                        for message in submissionsMAO:
                            print("\t\t\tSubmission Found")
                            f.write("\t\t\tSubmission Found\n")
                            messageCount+=1
                            fromEmail = find_From(service, message)
                            subjectLine = find_subject(service, message)
                            body = find_Bod(service, message)
                            try:
                                userID = subjectLine[len("MAO Submission "):subjectLine.rindex(" ")]
                                password = subjectLine[subjectLine.rindex(" ")+1:len(subjectLine)]
                                if check_user(userID, password, True):
                                    ugrade = check_user(userID, password, False)
                                    print("\t\t\t\tUploading info from UserID: " + userID + " and Password: " + password + " and Grade: " + ugrade)
                                    f.write("\t\t\t\tUploading info from UserID: " + userID + " and Password: " + password + " and Grade: " + ugrade + "\n")
                                    gradeID = search_for_file(serviceD, ugrade, "application/vnd.google-apps.folder", MAOID)
                                    try:
                                        studentID = search_for_file(serviceD, userID, "application/vnd.google-apps.folder", gradeID)
                                        unrevID = search_for_file(serviceD, "Unreviewed", "application/vnd.google-apps.folder", studentID)
                                        filepathimg = upload_submission(service, serviceD, message['id'], unrevID)
                                        print(filepathimg)
                                        tempfile = open(filepathimg + ".txt", "w+")
                                        tempfile.write(body)
                                        tempfile.close()
                                        upload_file(serviceD, filepathimg + ".txt", unrevID, "text/plain")
                                        os.remove(filepathimg + ".txt")
                                        mark_as_read(service, message)
                                        print("\t\tMessage " + str(messageCount) + ": Sending Data to " + fromEmail)
                                        f.write("\t\tMessage " + str(messageCount) + ": Sending Data to " + fromEmail + "\n")
                                        send_Message_Submission(service, fromEmail)
                                        os.remove(filepathimg)
                                    except:
                                        #create id folder and all subfolders (second api command in student screen)
                                        create_folder(serviceD, userID, gradeID)
                                        studentID = search_for_file(serviceD, userID, "application/vnd.google-apps.folder", gradeID)
                                        create_folder(serviceD, "Unreviewed", studentID)
                                        create_folder(serviceD, "Approved", studentID)
                                        create_folder(serviceD, "Disapproved", studentID)
                                        unrevID = search_for_file(serviceD, "Unreviewed", "application/vnd.google-apps.folder", studentID)
                                        filepathimg = upload_submission(service, serviceD, message['id'], unrevID)
                                        tempfile = open(filepathimg + ".txt", "w+")
                                        tempfile.write(body)
                                        tempfile.close()
                                        upload_file(serviceD, filepathimg + ".txt", unrevID, "text/plain")
                                        os.remove(filepathimg + ".txt")
                                        mark_as_read(service, message)
                                        print("\t\tMessage " + str(messageCount) + ": Sending Data to " + fromEmail)
                                        f.write("\t\tMessage " + str(messageCount) + ": Sending Data to " + fromEmail + "\n")
                                        send_Message_Submission(service, fromEmail)
                                        os.remove(filepathimg)
                                else:
                                    raise Exception("Username and Password did not match")
                            except Exception as e:
                                print("\t\tMessage " + str(messageCount) + ": Sending FAIL Data to " + fromEmail)
                                f.write("\t\tMessage " + str(messageCount) + ": Sending FAIL Data to " + fromEmail + "\n")
                                send_Message_Submission_Fail(service, fromEmail, str(e))
                                mark_as_read(service, message)
                        os.remove("userLoginValues.txt")
                #operations
                tasks = search_tasks(service)
                if tasks != []:
                    messageCount = 0
                    for message in tasks:
                        print("\t\t\tTask Found")
                        f.write("\t\t\tTask Found\n")
                        body = find_Bod(service, message)
                        fromEmail = find_From(service, message)
                        messageCount+=1
                        try:
                            if "NHS" in body:
                                print("\t\t\t\tNHS Task")
                                f.write("\t\t\t\tNHS Task\n")
                                NHSID = search_for_file(serviceD, "NHS", "application/vnd.google-apps.folder", None)
                                try:
                                    download_file(serviceD, search_for_file(serviceD, "userLoginValues.txt", "text/plain", NHSID), "userLoginValues.txt")
                                    cont = True
                                except:
                                    if cont:
                                        send_Message_Submission_Fail(service, "prabhukrish710@gmail.com", "The values file is unable to be retrived. Might be getting edits...")
                                    cont=False
                                if cont:
                                    if "Hours" in body:
                                        print("\t\t\t\tUploading info to: " + fromEmail + " Requesting Hours")
                                        f.write("\t\t\t\tUploading info to: " + fromEmail + " Requesting Hours\n")
                                        download_file(serviceD, search_for_file(serviceD, "studentHours.txt", "text/plain", NHSID), "studentHours.txt")
                                        send_message(service, fromEmail, "NHS Hours", "", "studentHours.txt")
                                        os.remove("studentHours.txt")
                                    elif "Send New Messages" in body:
                                        thread = threading.Thread(target=message_function(fromEmail, service, serviceD, NHSID))
                                        thread.start()
                                    elif "Login" in body:
                                        print("\t\t\t\tUploading info to: " + fromEmail + " Requesting Login")
                                        f.write("\t\t\t\tUploading info to: " + fromEmail + " Requesting Login\n")
                                        userID = body[len("Login NHS "):body.rindex(" ")]
                                        password = body[body.rindex(" ")+1:len(body)-2]
                                        if check_user(userID, password, True):
                                            send_message(service, fromEmail, "Validated Login True", "", "")
                                        else:
                                            send_message(service, fromEmail, "Validated Login False", "", "")
                                    elif "Opps" in body:
                                        download_file(serviceD, search_for_file(serviceD, "ops.txt", "text/plain", NHSID), "ops.txt") 
                                        send_message(service, fromEmail, "NHS Opps", "", "ops.txt")
                                        os.remove("ops.txt")
                                os.remove("userLoginValues.txt")
                            elif "MAO" in body:
                                print("\t\t\t\tMAO Task")
                                f.write("\t\t\t\tMAO Task\n")
                                MAOID = search_for_file(serviceD, "MAO", "application/vnd.google-apps.folder", None)
                                try:
                                    download_file(serviceD, search_for_file(serviceD, "userLoginValues.txt", "text/plain", MAOID), "userLoginValues.txt")
                                    cont = True
                                except:
                                    if cont:
                                        send_Message_Submission_Fail(service, "prabhukrish710@gmail.com", "The values file is unable to be retrived. Might be getting edits...")
                                    cont=False
                                if cont:
                                    if "Hours" in body:
                                        print("\t\t\t\tUploading info to: " + fromEmail + " Requesting Hours")
                                        f.write("\t\t\t\tUploading info to: " + fromEmail + " Requesting Hours\n")
                                        download_file(serviceD, search_for_file(serviceD, "studentHours.txt", "text/plain", MAOID), "studentHours.txt")
                                        send_message(service, fromEmail, "MAO Hours", "", "studentHours.txt")
                                        os.remove("studentHours.txt")
                                    elif "Send New Messages" in body:
                                        thread = threading.Thread(target=message_function(fromEmail, service, serviceD, MAOID))
                                        thread.start()
                                    elif "Login" in body:
                                        print("\t\t\t\tUploading info to: " + fromEmail + " Requesting Login")
                                        f.write("\t\t\t\tUploading info to: " + fromEmail + " Requesting Login\n")
                                        userID = body[len("Login MAO "):body.rindex(" ")]
                                        password = body[body.rindex(" ")+1:len(body)-2]
                                        if check_user(userID, password, True):
                                            send_message(service, fromEmail, "Validated Login True", "", "")
                                        else:
                                            send_message(service, fromEmail, "Validated Login False", "", "")
                                    elif "Opps" in body:
                                        download_file(serviceD, search_for_file(serviceD, "ops.txt", "text/plain", MAOID), "ops.txt") 
                                        send_message(service, fromEmail, "MAO Opps", "", "ops.txt")
                                        os.remove("ops.txt")
                                os.remove("userLoginValues.txt")
                            mark_as_read(service, message)
                        except Exception as e:
                            print("\t\tMessage " + str(messageCount) + ": Sending FAIL Data to " + fromEmail)
                            f.write("\t\tMessage " + str(messageCount) + ": Sending FAIL Data to " + fromEmail + "\n")
                            send_Message_Submission_Fail(service, fromEmail, str(e))
                            mark_as_read(service, message)
                #ai request
                incMessages = searching_Inc_Messages(service)
                if incMessages != []:
                    messageCount = 0
                    for message in incMessages:
                        messageCount+=1
                        fromEmail = find_From(service, message)
                        print("\t\tMessage " + str(messageCount) + ": Sending Data to " + fromEmail)
                        f.write("\t\tMessage " + str(messageCount) + ": Sending Data to " + fromEmail + "\n")
                        send_message_ai(service, fromEmail, find_Bod(service,message))
                        mark_as_read(service, message)
                if requests == [] and incMessages == [] and submissionsNHS == [] and tasks == [] and submissionsMAO == []:
                    print("\t\tNo Messages Found")
                    f.write("\t\tNo Messages Found\n")
                    if (counterS%10 == 0):
                        if(updateCount > 0): 
                            delete_file(serviceD, search_for_log_files(serviceD))
                        updateCount+=1
                        upload_log(serviceD, updateCount, logfolder)
                    time.sleep(10)
            except Exception as err:
                if "OverFrequency" not in str(err): 
                    errCounter+=1
                    print("There was an Error:\n" + str(err))
                    f.write("There was an Error:\n" + str(err)+"\n")
                    mixer.music.load("serveraudioE.mp3")
                    mixer.music.play()
                    while mixer.music.get_busy():  # wait for music to finish playing
                        time.sleep(1)
                    if errCounter >= 5:
                        f.close()
                        break
    except Exception as err:
        print("There was an Error:\n" + str(err))
        print("Critical Error, Server Offline")
        mixer.music.load("serveraudioE.mp3")
        mixer.music.play()
        while mixer.music.get_busy():  # wait for music to finish playing
            time.sleep(1)

if __name__ == '__main__':
    print("Program Starting")
    main()