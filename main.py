# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


import pyttsx3

engine = pyttsx3.init()


# Function to speak the given text
def speak(text):
    engine.say(text)
    engine.runAndWait()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # Example usage
    speak("Hello, how are you?")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
