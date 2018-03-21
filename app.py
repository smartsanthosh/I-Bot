from flask import Flask, render_template, request
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.trainers import ListTrainer
import urllib
app = Flask(__name__)

chatbot=ChatBot(
    'i-Bot',
    storage_adapter = "chatterbot.storage.MongoDatabaseAdapter",
    database = "i-bot",
    database_uri = "mongodb://Roy:"+urllib.parse.quote("Roy@123")+"@ds121309.mlab.com:21309/i-bot",
    logic_adapters=[
        "chatterbot.logic.BestMatch",
        'chatterbot.logic.MathematicalEvaluation',
    ]
    )

conversation=[
    "how are you",
    "iam fine"
]
chatbot.set_trainer(ListTrainer)
chatbot.train(conversation)
@app.route("/")
def home():
	return str(chatbot.get_response("how are you"))

@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    return str(chatbot.get_response(userText))


if __name__ == "__main__":
    app.run(debug=True)
