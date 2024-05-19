# -*- coding: utf-8 -*-
"""backend.ipynb"""


from flask import Flask as f, jsonify
from flask_cors import CORS
from tensorflow.keras.models import load_model
import random
import json
import numpy as np
import pickle
import nltk
# nltk.download('punkt')
# nltk.download('wordnet')
# nltk.download('omw-1.4')

from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()

# from keras.models import load model

# from flask import Flask

model = load_model('/Users/rthandra/Desktop/AIchatbot/AIchatbot_model_may4.h5')
intents = json.loads(
    open('/Users/rthandra/Desktop/AIchatbot/intents.json', encoding="utf8").read())
words = pickle.load(open('/Users/rthandra/Desktop/AIchatbot/word.pkl', 'rb'))
classes = pickle.load(
    open('/Users/rthandra/Desktop/AIchatbot/classes.pkl', 'rb'))


# preprocessing the words and tokenizing and converting it to lower case
def clean_sentence(sentence):
  sentence_words = nltk.word_tokenize(sentence)
  sentence_words = [lemmatizer.lemmatize(
      word.lower())for word in sentence_words]
  return sentence_words

# finds the match and sets it to 1 in bagOfWords


def bagOfWords(sentence, words, show_details=True):
  sentence_words = clean_sentence(sentence)
# bow is matrix of the no.of words
  bow = [0]*len(words)

  for s in sentence_words:  # contains the input sentence tokenize word
    for i, w in enumerate(words):  # contains word from word.pkl, i is the index no
      if (w == s):
        # if current word is in the dictionary assign 1 else put 0 in the ith index
        bow[i] = 1
        if show_details:
         print("found in bag: %s" % w)
  return (np.array(bow))


def class_check(sentence, model):
  predict_class = bagOfWords(sentence, words, show_details=False)
  result = model.predict(np.array([predict_class]))[0]
  error_threshold = 0.25
  results = [[i, r] for i, r in enumerate(result) if r > error_threshold]
  # sort strength by probability
  results.sort(key=lambda x: x[1], reverse=True)

  return_list = []
  for r in results:
    return_list.append({"intent": classes[r[0]], "probability": str(r[1])})

  return return_list

def receiveResponse(intens, intents_json):
    tag = intens[0]['intent']
    no_of_intents = intents_json['intents']
    for i in no_of_intents:
        if(i['tag']== tag):
            result_responses = random.choice(i['responses'])
            break
    return result_responses


def chatbot_response(message):
  intens = class_check(message, model)  # checks the tag
  res = receiveResponse(intens, intents)
  return res


app = f(__name__)
CORS(app)


@app.route("/", methods=['GET', 'POST'])
def hello():
    return jsonify({"health": "server is running"})


def decrypt(message):
    # convert the output by removing the plus and replace it with spaces
    string = message
    converted_string = string.replace("+", " ")
    return converted_string


@app.route('/query/<name>')
def query(name):

    # decrypt message
    # decrupts the message and sends it to the chatbot and converts the decrypted message into JSON format
    decrypt_msg = decrypt(name)

    response = chatbot_response(decrypt_msg)

    # json_object = ({"top_result":{"res":responses}})
    json_object = jsonify({"top": {"res": response}})
    return json_object

if __name__ == '__main__':
    app.run(port=3000)

'''
import os
import sys

from flask import Flask

def init_webhooks(base_url):
    # Update inbound traffic via APIs to use the public-facing ngrok URL
    pass

def create_app():
    app = Flask(__name__)

    # Initialize our ngrok settings into Flask
    app.config.from_mapping(
        BASE_URL="http://localhost:5000",
        USE_NGROK=os.environ.get("USE_NGROK", "False") == "True" and os.environ.get("WERKZEUG_RUN_MAIN") != "true"
    )

    if app.config["USE_NGROK"] and os.environ.get("NGROK_AUTHTOKEN"):
        # pyngrok will only be installed, and should only ever be initialized, in a dev environment
        from pyngrok import ngrok

        # Get the dev server port (defaults to 5000 for Flask, can be overridden with `--port`
        # when starting the server
        port = sys.argv[sys.argv.index("--port") + 1] if "--port" in sys.argv else "5000"

        # Open a ngrok tunnel to the dev server
        public_url = ngrok.connect(port).public_url
        print(f" * ngrok tunnel \"{public_url}\" -> \"http://127.0.0.1:{port}\"")

        # Update any base URLs or webhooks to use the public ngrok URL
        app.config["BASE_URL"] = public_url
        init_webhooks(public_url)

    # ... Initialize Blueprints and the rest of our app

    return app


USE_NGROK=True
NGROK_AUTHTOKEN = '2fuWItWNMsadTLou9vFHYqX5S6r_5jVNoE3YvcrwnUnPFtDgM'
FLASK_APP=server.py
flask run


from flask_ngrok import run_with_ngrok
from flask import Flask, jsonify

app_backend = Flask(__name__)
run_with_ngrok(app_backend)
#creating a route
@app_backend.route("/",methods=['GET'])
def hello(): #gets the question
  return jsonify({"health":"server is running"})

  def decrypt(message):
    #convert the output by removing the plus and replace it with spaces
    string = message
    converted_string = string.replace("+"," ")
    return converted_string

@app_backend.route("/query/<sentence>")
def query(sentence):


#decrypt
#decrupts the message and sends it to the chatbot and converts the decrypted message into JSON format
 decrypt_msg = decrypt(sentence)
 responses = chatbot_response(decrypt_msg)
 json_object = jsonify({"top_result":{"res":responses}})

 return json_object
app_backend.run()


'''
