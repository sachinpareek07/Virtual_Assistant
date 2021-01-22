# FEATURES SECTION

    # 1.DATE & TIME
    # 2.E-MAIL
    # 3.FAMILY
    # 4.GAMING
    # 5.Greetings
    # 6.JOKE
    # 7.MUSIC
    # 8.NOTe
    # 9.POWER OPTIONS
    # 10.SCREENSHOT
    # 11.Search Section
    # 12.Software
    # 13.WIKIPEDIA


# IMPORT SECTION
import json
import pyttsx3
import datetime
from datetime import date
import speech_recognition as sr
import wikipedia
import webbrowser
import os
import random
import smtplib
import subprocess
import pyautogui
import pyjokes
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice',voices[0].id)   #index[0] = mail voice & index[1] = female voice

# FUNCTIONS SECTION
a = 0
with open("Virtual_Assistant.json",'r') as d: #enter the path of the json file here
    params = json.load(d)["params"]
def speak(audio):
    engine.say(audio)
    engine.runAndWait()
def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good morning")
    elif hour>=12 and hour<18:
        speak("Good Afternoon")
    else:
        speak("Good evening")
    #speak("Hello sir ")

def wakeup():    
    r = sr.Recognizer()
    with sr.Microphone() as source: #(With)
        print("Listening....sir!")
        r.pause_threshold = 0.5
        audio = r.listen(source,phrase_time_limit=3)
    try:
        print("Recognizing sir....")
        query = r.recognize_google(audio,language="en-in")
        print("user said:",query,"\n")
    
    except Exception:
        return "None"
    return query

def takeCommand():
    #it takes microphone input and returns string output
    r = sr.Recognizer()
    with sr.Microphone() as source: 
        print("Listening....sir!")
        r.pause_threshold = 0.5
        audio = r.listen(source,phrase_time_limit=5)
    try:
        print("Recognizing sir....")
        query = r.recognize_google(audio,language="en-in")
        print("user said:",query,"\n")
    
    except Exception:
        speak("sir please can you repeat.....")
        return "None"
    return query
def notes(text):
    date = datetime.datetime.now()
    file_name = str(date).replace(':',"-") + "-note.txt"
    with open(file_name,"w") as f:
        f.write(text)
    subprocess.Popen(["notepad.exe",file_name])
def sendemail(to,content):
    server = smtplib.SMTP("smtp.gmail.com",587)
    server.ehlo()
    server.starttls()
    server.login(params["my_mail_id"],params["password"])
    server.sendmail(params["my_mail_id"],to,content)
    server.close()
def jokes():
    speak(pyjokes.get_joke())

## MAIN SECTION

if __name__ == "__main__":
    speak("hello sir")
    wishMe()
    while True:
        while True:
            listen = wakeup().lower()
            if "wake up" in listen: #->MAIN COMMAND<-
                speak("yes sir how can i help you")
                break
            if "stop" in listen:
                speak("ok sir")
                a = 1
                break
        if(a):
            break
        while True:
            query = takeCommand().lower()

            # DATE & TIME SECTION

            if "the time" in query:
                strTime = datetime.datetime.now().strftime("%H:%M:%S")
                speak(f"sir the time is {strTime}")
                break
            elif "date" in query:
                date = date.today()
                speak(f"sir    the    date    is       {date}")
                break
            elif "day" in query:
                day = date.today().strftime("%A")
                speak(f"sir    the    day    is       {day}")
                break

            # E-MAIL SECTION

            elif "send a mail" in query:            
                try:
                    speak("what should i say..?")
                    content = takeCommand()
                    to = params["mail1"]
                    sendemail(to,content)
                    speak("email has been sent")
                except Exception as e:
                    print(e)
                    speak("Sorry")
                break
            # GAMING SECTION

            elif "count the same letters" in query:
                speak("What is the word sir")
                word = takeCommand().lower()
                word = word.replace(" ","")
                count = 0
                for i in word:
                    c = word.count(i)
                    if c > 1:
                        count += 1
                print(count)
                speak(f"there are {count} same letters in {word}")
                break

            # GREETINGS SECTION

            elif "how are you" in query:
                speak("I'm good sir ")
                break

            # JOKE SECTION

            elif "tell me a joke" in query:
                jokes()
                break

            # MUSIC SECTION

            elif "play music" in query or "change music" in query:
                music_dir = params["music_path"]
                songs = os.listdir(music_dir)
                num = random.randint(0,len(songs))
                print("Playing the song :")
                os.startfile(os.path.join(music_dir,songs[num]))
                break
            
            # NOTe SECTION

            elif "make a note" in query:
                speak("What would you like me to write")
                note_text = takeCommand().lower()
                notes(note_text)
                speak("i've made a note of that")
                break

            # POWER OPTIONS SECTION
            
            elif "shutdown the pc" in query:
                os.system("shutdown /s /t 1")       #/r restart :: #/s shutdown
                break
                
            elif "go to sleep mode" in query:
                os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
                break

            ## SEARCH SECTION

            #1 YOUTUBE SEARCH SECTION

            elif "search on youtube" in query:
                speak("what should i search for you sir?")
                search = takeCommand().lower()
                webbrowser.open("https://www.youtube.com/results?search_query="+search)
                break
            
            #2 GOOGLE SEARCH
         
            elif "search something" in query:
                speak("what should i search for you sir?")
                searchR = takeCommand().lower()
                webbrowser.open("https://www.google.com/search?q="+searchR)
                break
            
            #4 SEARCH A LOCATION SECTION

            elif "find a location" in query:
                speak("What is the location")
                location = takeCommand()
                url = "https://google.nl/maps/place/" + location + '/&amp;'
                webbrowser.get().open(url)
                speak("Here it is")
                break
            # SCREENSHOT SECTION

            elif "take a screenshot" in query:
                myScreenshot = pyautogui.screenshot()
                myScreenshot.save(params["ss_path"])
                speak("Take a look sir")
                os.startfile(params["ss_path"])
                break
            
            # SOFTWARES SECTION

            elif "open spotify" in query:
                path = params["spotify"]
                os.startfile(path)
                break
            elif "open chrome" in query:
                path = params["chrome"]
                os.startfile(path)      
                break

            # WIKIPEDIA SECTION

            elif 'wikipedia' in query:
                speak("searching wikipedia.....")
                query = query.replace("wikipedia", "")
                results = wikipedia.summary(query,sentences=2)
                speak("According to wikipedia")
                print(results)
                speak(results)
                break
            elif "sleep" in query:
                speak("ok sir")
                break
            else:
                speak("sir please can you repeat")
                continue

#😊😊😊😊😊😊😊😊😊😊😊😊😊😊😊😊😊😊😊😊😊😊