from flask import Flask, render_template, request,jsonify
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.trainers import ListTrainer
import urllib
import json,requests
app = Flask(__name__)

chatbot=ChatBot(
    'i-Bot',
    storage_adapter = "chatterbot.storage.MongoDatabaseAdapter",
    database = "i-bot",
    database_uri = "mongodb://Roy:"+urllib.parse.quote("Roy@123")+"@ds121309.mlab.com:21309/i-bot",
    logic_adapters=[
        "chatterbot.logic.BestMatch",
        'chatterbot.logic.MathematicalEvaluation',
    ],
    read_only=True
    )

chatbot.set_trainer(ListTrainer)
conversation=[
"that's it",
"that's it"
]
chatbot.train(conversation)
@app.route("/")
def home():
	return render_template("speech.html")

@app.route("/api/chat", methods=['POST'])
def chat():
    userText = request.json['msg']
    response_message=(chatbot.get_response(userText))
    if response_message.confidence<0.75:
    	response_message="i don't know"
    else:
    	response_message=str(response_message)
    return jsonify(response=response_message)

@app.route("/api/learn", methods=['POST'])
def learn():
    print(request.json['msg'])
    conversation = request.json['msg']
    if len(conversation) !=2:
    	return jsonify(error="invalid no of conversations")
    else:
    	chatbot.train(conversation)
    	return jsonify(response="success")

headers = {
    "Content-Type": "application/json",
}

@app.route("/api/translate", methods=['POST'])
def translate():
	resp = requests.request("POST","https://translate.yandex.net/api/v1.5/tr.json/translate ?key=trnsl.1.1.20180321T182122Z.0744c55b609c1cca.0377b6bfa4fd2ff3b9efb061d71df78173b6a017& text="+request.json["text"]+"& lang="+request.json["from"]+"-"+request.json["to"], headers=headers)
	return jsonify(json.loads(resp.content))

@app.route("/api/image_classifier", methods=['POST'])
def image_classifier():
	api_key = 'acc_a8a69b84e97af11'
	api_secret = '97eed8248a51c9feaf65e172ee9010e8'
	image = request.files['image']
	print(image.read().decode('utf-8'))
	response = requests.post('https://api.imagga.com/v1/content',
	auth=(api_key, api_secret),
	files={'image': image.read().decode('utf-8')})
	return jsonify(json.loads(response.content.decode("utf-8")))


if __name__ == "__main__":
    app.run(debug=True)
