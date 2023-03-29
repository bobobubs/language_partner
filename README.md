<!-- @format -->

# language_partner

A basic interactive language partner that interacts with ChatGPT.
Currently only specified for chinese. Other languages are possible but may lead to undefined behavior.

## Installing Rquirements

`pip install -r requirements.txt`

## Adding your API Key

Add your OpenAI secret key to the secret variable in credentials.py

## Running the app

`python .\chat.py`

This will prompt you for your language. Just write it our in english. E.g. Chinese.
After it will prompt you for you experience in the language on a scale from 1-5
From that point on your conversation will begin. Responses will be played out as audio. For Chinese, the pinyin for the responses will also be displayed.
After the audio is finished you will be able to type your own responses and continue the conversation.
