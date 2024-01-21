import speech_recognition as sr
import pyttsx3
from random import choice
import datetime
import requests
import platform
import subprocess

class RubyVoiceAI:
    def __init__(self):
        self.check_dependencies()
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.engine = pyttsx3.init()
        self.commands = {
            "What time is it": self.get_time,
            "flip a coin": self.flip_coin,
            "roll a dice": self.roll_dice,
            "give me a compliment": self.give_compliment,
            "what are your commands": self.list_commands,
            "what can you do": self.list_commands,
            "what is your purpose": self.list_commands
        }

    def check_dependencies(self):
        required_dependencies = ["speech_recognition", "pyttsx3", "requests"]

        for dependency in required_dependencies:
            try:
                # Check if the dependency is already installed
                __import__(dependency)
            except ImportError:
                print(f"Installing {dependency}...")
                self.install_dependency(dependency)
    
    def install_dependency(self, dependency):
        try:
            subprocess.check_call(["pip", "install", dependency])
            print(f"{dependency} installed successfully.")
        except subprocess.CalledProcessError:
            print(f"Failed to install {dependency}. Please install it manually.")

    def listen_for_command(self):
        with self.microphone as source:
            print("Listening...")
            audio = self.recognizer.listen(source, timeout=None)  # Wait indefinitely

        try:
            command = self.recognizer.recognize_google(audio).lower()
            print("Heard:", command)

            if "goodbye" in command:
                print("Goodbye!")
                self.speak("Goodbye!")
                exit()  # Terminate the program

            elif "ruby" in command:
                # If the command contains "ruby", remove it before executing
                command = command.replace("ruby", "").strip()
                self.execute_command(command)

            else:
                print("Command not recognized. Please try again.")

        except sr.UnknownValueError:
            print("Sorry, could not understand the audio.")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")

    def execute_command(self, command):
        command_lower = command.lower()
        found_command = None

        for keyword, function in self.commands.items():
            if keyword.lower() in command_lower:
                found_command = keyword
                break

        if found_command:
            result = self.commands[found_command]()
            print(result)
            self.speak(result)
        else:
            print("Command not recognized. Please try again.")

    def get_time(self):
        now = datetime.datetime.now()
        formatted_time = now.strftime('%I:%M %p')  # %I for 12-hour format, %M for minutes, %p for AM/PM
        return f"The current time is {formatted_time}."

    def flip_coin(self):
        result = choice(["Heads", "Tails"])
        return f"The coin landed on {result}."

    def roll_dice(self):
        result = choice([1, 2, 3, 4, 5, 6])
        return f"The dice rolled a {result}."

    def give_compliment(self):
        try:
            response = requests.get("https://raw.githubusercontent.com/iMercilessly/RubyAI/main/compliments.txt")
            compliments = response.text.splitlines()

            if compliments:
                random_compliment = choice(compliments)
                return random_compliment
            else:
                return "No compliments available at the moment."

        except requests.RequestException as e:
            return f"Error fetching compliments: {e}"

    def list_commands(self):
        return "I can do the following: What time is it?, Flip a coin, Roll a dice, Give me a compliment."

    def speak(self, text):
        if platform.system() == 'Darwin':
            self.engine = pyttsx3.init(driverName='nsss')  # Use NSSpeechSynthesizer driver on macOS
        else:
            self.engine = pyttsx3.init()

        # Changing the voice to the second voice in the list (if available)
        voices = self.engine.getProperty('voices')
        if len(voices) > 1:
            self.engine.setProperty('voice', voices[1].id)

        # Changing the rate to a slower pace (adjust as needed)
        self.engine.setProperty('rate', 150)

        self.engine.say(text)
        self.engine.runAndWait()

if __name__ == "__main__":
    ruby = RubyVoiceAI()

    while True:
        ruby.listen_for_command()
