import openai
import pyttsx3
import pinyin
from translate import Translator
from creds import init_prompt, secret

# Set up the OpenAI API client
openai.api_key = secret

# Set up the models and prompt
model_engine = "text-davinci-003"
speech_engine = pyttsx3.init()
#translator= Translator(to_lang="English")
speech_engine.setProperty('voice', "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_ZH-CN_HUIHUI_11.0")

init_prompt += input("What language would you like to speak in: \n")
init_prompt += input("What level is your experiece (1-5): \n")
# Generate a response
completion = openai.Completion.create(
    engine=model_engine,
    prompt=init_prompt,
    max_tokens=1024,
    n=1,
    stop=None,
    temperature=0.5,
)

response = completion.choices[0].text
print(type(response))
print(response)
print(pinyin.get(response, delimiter = ' '))
#print(translator.translate(response))
speech_engine.say(response)
speech_engine.runAndWait()

while True:
    prompt = input(">>> ")

    # Generate a response
    completion = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )
    
    response = completion.choices[0].text
    print(response)
    print(pinyin.get(response, delimiter = ' '))
    #print(translator.translate(response))
    speech_engine.say(response)
    speech_engine.runAndWait()