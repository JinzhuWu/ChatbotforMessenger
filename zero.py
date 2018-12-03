import random
from flask import Flask, request
from pymessenger.bot import Bot
import os 
import app
import NLP

zero = Flask(__name__)
ACCESS_TOKEN = 'EAAe93RZCKQZC4BAKkwb0Jx1JIZCJWDCZCOV6HZCt8gMyZC7ZC1tUeSVjkmZBnlpOJVw20rAtvL4fMeuWZALs0KWeB3TsZAMh8bFqlZBrjpuv5ObUgtI0lp8246QiYgMFJdghPYFyWHkzYIzxeNkjpxpDZB5vEi9vGV9VrACr9UZAOGrlaL36SVrIWlcxzLz9UWihw8E4ZD'   #ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
VERIFY_TOKEN = 'ChatBotZero'   
bot = Bot (ACCESS_TOKEN)

#receive messages that Facebook sends the bot at this endpoint 
@zero.route("/", methods=['GET', 'POST'])
def receive_message():
    if request.method == 'GET':
        # Implemented a verify token that confirms all requests that our bot receives came from Facebook Messenger.
        token_sent = request.args.get("hub.verify_token")
        return verify_fb_token(token_sent)
    if request.method == 'POST':
       output = request.get_json()
       for event in output['entry']:
          messaging = event['messaging']
          for message in messaging:
            if message.get('message'):
                # Get Facebook Messenger ID in order that we can send response back
                recipient_id = message['sender']['id']
                session_id = message['recipient']['id'] # backend id
                if message['message'].get('text'):
                    # Get the content of users, we need deal with those questions
                    sender_text = message['message']['text'].lower()
                    # set up connection with apiai, send questions to dialogflow for NLP, return keyword, intent, and confidence
                    text_list = NLP.sentence_tokens(sender_text)
                    for i in range(len(text_list)):
                        query,result,confidence = app.get_intent(text_list[i])
                        # Get the response content
                        response_sent_text, send_content = get_message(query,result,confidence)
                        # Send the message to users
                        send_message(recipient_id, response_sent_text,send_content)
                # if user sends us a non-text item
                if message['message'].get('attachments'):
                    response_sent_nontext = "Sorry, I haven't learned to read nontext questions. Can you ask questions in text?"
                    send_content = 'text'
                    send_message(recipient_id, response_sent_nontext,send_content) #need to change
    return "Message Processed!"


def verify_fb_token(token_sent):
    #take token sent by facebook and verify it matches the verify token we sent
    #if it is a correct verify token, allow the request and deal with this request 
    # else return an error information
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token!'

#sample response: just chooses a random message to send to the user
def get_message(query,result,confidence):
    send_content = 'text'
    response = result

    if response == 'map':
        send_content = 'map'
    if response == 'hours':
        send_content = 'hours'
    if response == 'visitor':
        send_content = 'visitor'
    if response == 'printprice':
        send_content = 'printprice'
        # if response == 'tutorial':
        #     send_content = 'tutorial'
    if confidence < 0.5 or response == 'Sorry, I did not get it.':
        new_words = NLP.preprocessing(query)
        if 'fine' in new_words:
            send_content = 'fine'
        if 'food' in new_words:
            send_content = 'food'
        if 'borrow' in new_words or 'book' in new_words:
            send_content = 'borrow'
        if 'room' in new_words:
            send_content = 'room'
        if 'print' in new_words:
            send_content = 'print'
        if 'account' in new_words:
            send_content = 'account'
        else:
            foo = ['Sorry, this may be beyond the scope I understand.','Sorry, I did not get it.','Can you describe this question in other ways?','Sorry, I can not understand, please ask questions about the UNSW library.']
            response = random.choice(foo)

    return response,send_content

#uses PyMessenger to send response to user
def send_message(recipient_id, response,send_content):
    #sends user the text message provided via input response parameter
    if send_content == 'text':
        bot.send_text_message(recipient_id, response)
    if send_content == 'map':
        # answers = 'Here is the map of UNSW Kensington Campus. Hope it can help you.'
        answers = 'Here is the map of UNSW Kensington Campus. Hope it can help you.'
        image_path = 'http://funkyimg.com/i/2LEGH.png'
        bot.send_image_url(recipient_id, image_path)
        bot.send_text_message(recipient_id, answers)
    if send_content == 'hours':
        answers = 'This is the opening hours of the library. Please arrange your time well.'
        image_path = 'http://funkyimg.com/i/2LEGJ.png'
        bot.send_image_url(recipient_id, image_path)
        bot.send_text_message(recipient_id, answers)
    if send_content == 'printprice':
        image_path = 'http://funkyimg.com/i/2LKLo.png'
        bot.send_image_url(recipient_id, image_path)
    if send_content == 'fine':
        answers = 'You can click this link to get more information about fines and fines rates: www.library.unsw.edu.au/study/borrowing/fines'
        bot.send_text_message(recipient_id, answers)
    if send_content == 'food':
        answers = 'You can find out the policies and guidelines about food requirements in the library by this link: www.library.unsw.edu.au/study/about-unsw-library/policies-and-guidelines/food-in-the-library'
        bot.send_text_message(recipient_id, answers)
    if send_content == 'borrow':
        answers = 'I am not sure which question you want to ask about borrowing book. The following link provides more guidance on borrowing books, including request, renew, recall, return and rights: www.library.unsw.edu.au/study/borrowing'
        bot.send_text_message(recipient_id, answers)
    if send_content == 'room':
        answers = 'You can do this by logging into the UNSW Room Bookings System. Bookings should be made by UNSW Students only. Here is the link: https://roombookings.library.unsw.edu.au'
        bot.send_text_message(recipient_id, answers)
    if send_content == 'account':
        answers = 'Please log in UNSW Online Account System to implement more operation: https://recharge.it.unsw.edu.au/mymonitor/'
        bot.send_text_message(recipient_id, answers)
    if send_content == 'print':
        answers = 'Here is the guidelines about Campus Printers. You can find more details for Print/Copy/Scan: https://www.it.unsw.edu.au/students/mps/'
        bot.send_text_message(recipient_id, answers)
    if send_content == 'visitor':
        answers = 'If you are not from UNSW, please review this guidelines to get more information: www.library.unsw.edu.au/study/not-from-unsw'
        bot.send_text_message(recipient_id, answers)
    return "success!"

if __name__ == "__main__":
    zero.run()
