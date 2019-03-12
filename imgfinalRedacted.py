import requests  
import json
from bottle import (  
    run, post, response, request as bottle_request
)
BOT_URL = 'REDACTED' # <--- add your telegram token here; it should be like https://api.telegram.org/bot12345678:SOMErAn2dom/
def get_chat_id(data):  
    """
    Method to extract chat id from telegram request.
    """
    chat_id = data['message']['chat']['id']
    return chat_id
def file_id(data):
    """
    Method to extract file_id from telegram request.
    """
    file_id = data['message']['voice']['file_id']
    return file_id
def send_message(prepared_data):
    """
    Prepared data should be json which includes at least `chat_id` and `text`
    """ 
    message_url = BOT_URL + 'sendMessage'
    requests.post(message_url, json=prepared_data)  # don't forget to make import requests lib
# def change_text_message(text):  
#     """
#     To enable turning our message inside out
#     """
#     return text[::-1]
def process_audio(audio_id):
    url = "http://52.163.240.180/client/dynamic/recognize"
    headers = {'content-type': 'audio/ogg'}
    print(audio_id)
    file_id = requests.get(BOT_URL + "getFile?file_id=" + audio_id).json()['result']['file_path']
    print(file_id)
    audiofile = requests.get('REDACTED' + file_id)
    r = requests.put(url, data=audiofile, headers=headers).json()
    print(r)
    print(r['hypotheses'][0]['utterance'])
    return r['hypotheses'][0]['utterance']

def prepare_data_for_answer(data):  
    answer = process_audio(file_id(data))
    json_data = {
        "chat_id": get_chat_id(data),
        "text": answer,
    }
    return json_data

def prepare_data_for_feedback(data):  
    json_data = {
        "chat_id": get_chat_id(data),
        "text": "Nice one! Hang on, is this what u said? Pls correct me if I'm wrong sia..",
    }
    return json_data

def prepare_data_for_points(data):  
    json_data = {
        "chat_id": get_chat_id(data),
        "text": "swee! +10 points, come back more often to challenge the SINGLISH caption king!!!",
    }
    return json_data

def get_feedback(data):
    text = data['message']['text']  #to be collected the correct Singlish text

#x = 0
def img(data):
#    if x > 0: 
#        return
#    x = 1
    chat_id = get_chat_id(data)
    get_image = requests.get('https://random.dog/woof.json').json()
    image_url =get_image['url']
    print(image_url)
    json_data = {
        "chat_id": get_chat_id(data),
        "photo": image_url,
    }
    message_url = BOT_URL + 'sendPhoto'
    requests.post(message_url, json=json_data)  # don't forget to make import requests lib


def wait_reply(data):
    json_data = {
        "force_reply": "true",
    }
    print("WAITING FOR REPLY")
    message_url = BOT_URL + 'ForceReply'
    requests.post(message_url, json = json_data)

@post('/')
def main():  
    data = bottle_request.json
    print(data)
    if('text' in data['message']):
        if(data['message']['text'] == '/image'):
            #send an image
            img(data)
            image_sent = "True"
        else:
             #collect a corrected sentence
            get_feedback(data)
            points_data =  prepare_data_for_points(data)
            send_message(points_data)
    elif('voice' in data['message']):
        #collect a sound
        answer_data = prepare_data_for_answer(data) 
        feedback_data = prepare_data_for_feedback(data)
        send_message(feedback_data)
        send_message(answer_data)  # <--- function for sending answer
   
    return response  # status 200 OK by default

if __name__ == '__main__':  
    run(host='localhost', port=8090, debug=True)
