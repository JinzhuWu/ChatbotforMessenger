# -*- coding: utf-8 -*-
import os.path, sys
import json
import chardet

def get_intent(query):
    # print(query)
    #print(chardet.detect(query))

    try:
        import apiai
    except ImportError:
        sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
        import apiai

    CLIENT_ACCESS_TOKEN = 'd8e85013d2b240868188d74d9d189586'
    ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)

    request = ai.text_request()

    request.lang = 'en' # default value equal 'en' - English
    if isinstance(query,str):
        request.query = query
    else:
        request.query = query.decode("utf-8")
    
    new_response = json.loads(request.getresponse().read().decode('utf-8','ignore'))
    # print("--------------")
    # print(new_response)
    # print("--------------")

    # keyword = new_response["result"]["parameters"]
    # intent = new_response["result"]["metadata"]["intentName"]
    confidence = new_response["result"]["score"]
    result = new_response["result"]["fulfillment"]["speech"]
    return query,result,confidence
#a=b"how are you"
#print(get_intent(a.decode("utf-8")))