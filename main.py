# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, jsonify
import os,sys
import app as A

app = Flask(__name__)

@app.route("/")
def hello():
    return render_template('chat.html')

@app.route("/ask", methods=['POST'])
def ask():
   message = request.form['messageText'].encode('utf-8').strip()
   
   while True:
       if message == "quit":
           exit()
       else:
           #bot_response = kernel.respond(message)
           #print (bot_response)
           query,bot_response,confidence = A.get_intent(message.lower())
           return jsonify({'status':'OK','answer':bot_response})
       
if __name__ == "__main__": 

    app.debug = True
    app.run(host='127.0.0.1', port=5001, debug=True)
