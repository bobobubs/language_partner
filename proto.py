import pyttsx3

engine = pyttsx3.init()
engine.setProperty('voice', "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_ZH-CN_HUIHUI_11.0")

while True:
    toSay = input("What would you like to hear?: \n")
    engine.say(toSay)
    engine.runAndWait()
    