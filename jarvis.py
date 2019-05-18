import wikipedia
import datetime
import re
import pyttsx3
import speech_recognition as sr
import webbrowser
"""To open webbrowser and put url in it"""
"""Python Speech recognition module, I used google speech to text engine through it."""
"""pyttsx3 creates engine for text to speech, I used microsoft SAPI5 engine to make my program speak"""
"""re stands for regex expression. I imported it to easily replace space with plus."""
"""Imported datetime to get date and time."""


class Jarvis():
    def __init__(self, voice=1):
        """Initialize microsoft sapit5 as engine for text to speech conversion and by defaut use zira voice ,Pass 0 argument to use David voice"""
        self.engine = pyttsx3.init("sapi5")
        self.voices = self.engine.getProperty("voices")
        self.engine.setProperty("voice", self.voices[voice].id)

    def speak(self, string):
        """Use Engine to say string and then print it"""
        self.engine.say(string)
        self.engine.runAndWait()
        print(string)

    def greet_user(self):
        """greet user based on time"""
        hour = int(datetime.datetime.now().hour)
        if hour >= 0 and hour < 12:
            self.speak("Good Morning")
        elif hour >= 12 and hour <= 16:
            self.speak("Good Afternoon")
        else:
            self.speak("Good Evening")
        self.speak("How may I help you?")

    def take_input(self):
        """Take voice input and recognize it"""
        r = sr.Recognizer() # creates a Recognizer class to recognize speech
        with sr.Microphone() as source: #Use microphone to listen to audio
            r.pause_threshold = 1.5
            r.energy_threshold = 6429.040451770137 # set it according to your noice level This working fine for me
            while True:
                self.speak("listening...")
                audio = r.listen(source, timeout=5, phrase_time_limit=20)
                try:
                    # self.speak("recognizing...")
                    query = r.recognize_google(audio, language="en-in") #The audio recorded is sent to google to recognizee
                    # self.speak(f"User Said: {query}")
                except Exception as e:
                    self.speak(e)
                    self.speak("Please say that again...")
                    continue
                # print(query)
                return query

    def search(self, word, search_string):
        """Used to search any website"""
        # self.speak(f"Tell me the words to search {word}:")
        search_string = search_string.replace(f"search {word}","")
        search_string = re.sub(" ", "+", search_string)
        webbrowser.open(f"www.{word}.com/search?q={search_string}")

    def search_wikipedia(self,word, search_string):
        """Used to search wikipedia"""
        search_string = search_string.replace(f"search {word}","")
        results = wikipedia.summary(search_string,sentences=4)
        self.speak(results)
    def timeanddate(self):
        """Used datetime module to print date and time"""
        time = datetime.datetime.now()
        self.speak(f"Today is {time.day}/{time.month}/{time.year}.Time is {time.hour}:{time.minute}:{time.second}")

    def main(self):
        """Main Function from where other functions are called"""
        self.greet_user()
        while True:
            query = self.take_input()
            if "search google" in query.lower():
                self.search("google",query.lower())
            elif "search youtube" in query.lower():
                self.search("youtube",query.lower())
            elif "search wikipedia" in query.lower():
                self.search_wikipedia(wikipedia,query.lower())
            elif "time" in query.lower():
                self.timeanddate()
            elif "exit" in query.lower() or "goodbye" in query.lower():
                if datetime.datetime.now().hour > 19 or datetime.datetime.now().hour <= 5:
                    self.speak("goodnight")
                else:
                    self.speak("goodbye")
                break

if __name__ == "__main__":
    Jarvis().main()