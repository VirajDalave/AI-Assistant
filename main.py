import speech_recognition as sr
import os
import webbrowser
import datetime
import subprocess
import openai
from config import apikey
import pywhatkit


def say(text):
    os.system(f'"wsay "{text}" --voice 6 "')

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=1)
        r.pause_threshold = 1

        audio = r.listen(source)
        try:

            query = r.recognize_google(audio, language="en-in")
            print(f"user said: {query}")
            return query

        except Exception as e:
            return "Sorry I couldn't hear you"

def searchOnYoutube(query):
    words = query.lower().split(" ")
    ytindex = int(words.index("youtube"))
    siteend = ""
    for index in range(ytindex + 1, len(words)):
        siteend += f"+{words[index]}"

    site = "https://www.youtube.com/results?search_query=" + (siteend[1:])
    say(f"Searching for {words[ytindex+1:]} on youtube")
    webbrowser.open(site)


def searchOnGoogle(query):
    searchitem = f"{''.join(query.lower().split('google')[1:]).strip()}"
    say(f"Searching {searchitem} on google")
    pywhatkit.search(searchitem)

def whatsAppMsg(query):
    message = f"{''.join(query.lower().split('whatsapp')[1:]).strip()}"

    say("to whom")
    try:
        print("Listening...")
        number = f"+91{takeCommand()}"
        say(f"Sending {message} on whatsapp")
        pywhatkit.sendwhatmsg_instantly(number, message, 10, )
    except Exception as e:
        print("Please try again")


def play(query):
    song = query.lower().split('play')[1:]
    pywhatkit.playonyt(song)
    say(f"playing {song}")

def ai(query):
    openai.api_key = apikey
    text=""

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=query,
        temperature=0.7,
        max_tokens=128,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    text += response['choices'][0]['text']
    if not os.path.exists("Openai"):
        os.mkdir("Openai")

    try:
        with open(f"Openai/{''.join(query.split('intelligence')[1:]).strip()}.txt","w") as f:
            f.write(text)
    except Exception as e:
        print("Some Error Occured")


chatStr=""
def chat(query):
    global chatStr
    print(chatStr)
    openai.api_key = apikey
    chatStr+=f"Viraj: {query} \n AI: "
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "user",
                    "content": query
                }
            ],
            temperature=1,
            max_tokens=128,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
    except Exception:
        return "Some Error Occuredd"

    chatStr += f"{response['choices'][0]['message']['content']}\n"
    print(chatStr)
    say(response["choices"][0]["message"]["content"])

    return response["choices"][0]["message"]["content"]


if __name__ == '__main__':
    say("Welcome")

    while True:
        print("Listening...")
        query = takeCommand()

        sites=[["youtube","https://www.youtube.com"],["wikipedia","https://www.wikipedia.com"],["gcr","https://classroom.google.com/u/1/h?pli=1"]]
        for site in sites:
            if f"Open {site[0]}".lower() in query.lower():
                say(f"Opening {site[0]}")
                webbrowser.open(site[1])
                exit()


        if "search on youtube" in query.lower():
            searchOnYoutube(query)
            exit()

        elif "search on google" in query.lower():
            searchOnGoogle(query)
            exit()

        elif "on whatsapp" in query.lower():
            whatsAppMsg(query)
            exit()


        elif "the time" in query.lower():
            time = datetime.datetime.now().strftime("%H:%M:%S")
            print(f"The time is {time}")
            say(f"The time is {time}")

        elif "open vs code" in query.lower():
            subprocess.run("C:\\Users\Viraj Dalave\AppData\Local\Programs\Microsoft VS Code\Code.exe")
            exit()

        elif "using artificial intelligence" in query.lower():
            ai(query)

        elif "play" in query.lower():
            play(query)
            exit()

        elif "reset chat" in query.lower():
            chatStr=""

        else:
            print("Chatting...")
            chat(query)
