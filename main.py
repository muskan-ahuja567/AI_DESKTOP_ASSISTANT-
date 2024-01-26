import speech_recognition as sr
import pyttsx3 as p
import webbrowser
import subprocess
import keyboard
import os
import time
import datetime
import smtplib
import requests

def say(text):
    engine = p.init()
    engine.say(text)
    engine.runAndWait()


def take_command():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening..")
        recognizer.adjust_for_ambient_noise(source)
        recognizer.pause_threshold = 1
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        print(f"You said: {text}")
        say(text)
        return text
    except sr.UnknownValueError:
        print("Sorry, could not understand audio.")
        say("Sorry, could not understand audio.")
        return "Sorry, could not understand audio."
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        say("Error in recognizing speech.")
        return "Error in recognizing speech."


def close_application(app_name):
    platform = os.name
    if platform == "nt":
        time.sleep(5)
        os.system(f'taskkill /f /im "{app_name}.exe"')


def send_email(subject, body, to_email):
    gmail = "muskan.ahuja365@gmail.com"
    password = "evrf uyew cqwq gxgs"
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(gmail, password)
            server.sendmail(gmail, to_email, f"Subject: {subject}\n\n{body}")
        return True
    except Exception as e:
        print(f"An error occurred: {e}")
        return False


def get_weather(api_key, city):
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {'q': city, 'appid': api_key, 'units': 'metric'}
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        data = response.json()
        temperature = data['main']['temp']
        description = data['weather'][0]['description']
        print(f'Temperature: {temperature}°C, Description: {description}')
        say(f"Temperature is {temperature}")
    else:
        print(f'Error: {response.status_code}')


def get_current_affairs(a_key):
    url = "https://newsapi.org/v2/top-headlines"
    params = {'apiKey': a_key, 'country': 'in', 'pageSize': 1}
    response = requests.get(url, params=params)
    data = response.json()
    articles = data.get('articles', [])
    current_affairs_text = ""
    for article in articles:
        title = article.get('title', '')
        description = article.get('description', '')
        current_affairs_text += f"{title}. {description}. "

    return current_affairs_text

if __name__ == "__main__":
    print("Hello, I am your personal assistant. How can I help you?")
    say("Hello, I am your personal assistant. How can I help you?")
    query = take_command()
    while True:
        if "Open site".lower() in query.lower():
            print("Which site do you want to open?")
            say("Which site do you want to open?")
            query1 = take_command()
            sites = [["Youtube", "https://youtube.com"], ["Wikipedia", "https://wikipedia.org"], ["Google", "https://google.com"] ]
            for site in sites:
                if f"Open {site[0]}".lower() == query1.lower():
                    print(f"Opening {site[0]}..")
                    say(f"Opening {site[0]}")
                    webbrowser.open(site[1])

        elif "Open an application".lower() in query.lower():
            print("Which application do you want to open?")
            say("Which application do you want to open?")
            query2 = take_command()
            commands = [["Outlook", r"C:\\Program Files (x86)\\Microsoft Office\\root\\Office16\\OUTLOOK.EXE"], ["MS Word", r"C:\\Program Files (x86)\\Microsoft Office\\root\\Office16\\WINWORD.EXE"]]
            for command1 in commands:
                if f"Open {command1[0]}".lower() in query2.lower():
                    print(f"Opening {command1[0]}..")
                    say(f"Opening {command1[0]}")
                    subprocess.Popen([command1[1]])
        elif "play music" in query:
            i = 1
            musicPath = f"C:\\Users\\HP\\Music\\{i}.mp3"
            process = subprocess.Popen(["start", musicPath], shell=True)
            while True:
                print("Say 'Stop' to pause, 'Play' to play, 'Change Music' to change, 'Exit' to Quit and 'Close' to exit the application\n")
                command = take_command()
                if command.lower() == "stop":
                    keyboard.press_and_release('space')
                elif command.lower() == "play":
                    keyboard.press_and_release('space')
                elif command.lower() == "change music":
                    i = i+1
                    musicPath = f"C:\\Users\\HP\\Music\\{i}.mp3"
                    process = subprocess.Popen(["start", musicPath], shell=True)
                elif command.lower() == "exit":
                    break
                elif command.lower() == "close":
                    app_name = "wmplayer"
                    close_application(app_name)
                else:
                    pass

        elif "what is the time" in query:
            h = datetime.datetime.now().strftime("%H")
            m = datetime.datetime.now().strftime("%M")
            s = datetime.datetime.now().strftime("%S")
            print(f"The time is {h} hours {m} minutes and {s} seconds")
            say(f"The time is {h} hours {m} minutes and {s} seconds")

        elif "Send an email".lower() in query.lower():
            print("Please say the email subject.")
            say("Please say the email subject.")
            subject = take_command()
            print("Please say the email body.")
            say("Please say the email body.")
            body = take_command()
            to_email = "tarunchaturvedi686@gmail.com"
            success = send_email(subject, body, to_email)
            if success:
                print("Email sent successfully!")
                say("Email sent successfully!")
            else:
                print("There was an error sending the email. Please check your credentials.")
                say("There was an error sending the email. Please check your credentials.")

        elif "Give me weather update".lower() in query.lower():
            api_key = "0ff352134f91d97a673f1e44270286be"
            city = input("Enter the city")
            get_weather(api_key, city)

        elif "News".lower() in query.lower():
            api_key = "9bca1e0b0ead47998855144a82bec18b"
            news = get_current_affairs(api_key)
            say(news)
        else:
            print("Sorry, something went wrong")
            say("Sorry something went wrong")
            break

        print("Do you need my further assistance?")
        say("Do you need my further assistance?")
        query = take_command()









