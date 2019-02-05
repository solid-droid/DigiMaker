import json

import os

import requests

from flask import Flask,request,make_response

from flask_cors import CORS

 

#########

import os.path

try:

    import apiai

except ImportError:

    sys.path.append(

        os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)

    )

    import apiai

 

CLIENT_ACCESS_TOKEN = 'd10f0b7511324498876f138eab989b6c'

#########

# Flask app should start in global layout

globvar = 1

speech=""

app = Flask(__name__)

cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

 

@app.route('/query',methods=['GET'])

def query():

                que=request.args.get('query')

                ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)

                req = ai.text_request()

                req.lang = 'de'  # optional, default value equal 'en'

                req.session_id = "fc63f34a2bfd4ed9bc9f3cefb5410222"

                req.query = que

                response = req.getresponse()

                response = response.read()

                print(response)

                return response
                

@app.route('/webhook', methods=['POST'])

def webhook():

                req = request.get_json(silent=True, force=True)

                print ("Request:")

                print(json.dumps(req, indent=4))

                res = makeWebhookResult(req)

                res = json.dumps(res, indent=4)

                print(res)

                r = make_response(res)

                r.headers['Content-Type'] = 'application/json'

                return r

 

def makeWebhookResult(req):

                global year

                global speech

                global amount

                global var2

                # print(req)

                m=req.get("result").get("action")

                print ("I am in webhook")

                query=req.get("result").get("resolvedQuery")

                print("******************",req.get("result").get("metadata").get("intentName"))

                url = "http://ayushpalak.pagekite.me"

                if req.get("result").get("metadata").get("intentName") == "OpenIntent":

                                print("Starting")

                                #speech = ""

                elif req.get("result").get("metadata").get("intentName") == "InvestmentIntent":

                                               

                                year=req.get("result").get("parameters").get("year").get("amount")

                                print("--------------------------------------------------------")

                                print(year)

                                print("--------------------------------------------------------")

                                amount=req.get("result").get("parameters").get("amount")

                                print("--------------------------------------------------------")

                                print(amount)

                                print("--------------------------------------------------------")

                                payload = '{"amount" : '+str(amount)+',"years" :'+str(year)+'}'

                                print(payload)

                                headers = {

                                                'content-type': "application/json" }

                                response = requests.request("POST", url, data=payload, headers=headers)

                                result = {}

                                result = response.json()

                                print(response.text)

                                speech="As per portfolio, here are the top three stocks. 1. American Bank @"+result['american bank'][3]+"% interest rate with "+result['american bank'][2]+" return, "+result['american bank'][1]+" risk. 2. British Bank @ "+result['british bank'][3]+" % interest rate with "+result['british bank'][2]+" return, "+result['british bank'][1]+" risk. 3. Wells sachs Bank @ "+result['wells sachs'][3]+" % interest rate with "+result['wells sachs'][2]+" return, "+result['wells sachs'][1]+" risk. which among these you want to choose?"

                                print(speech)

                elif req.get("result").get("metadata").get("intentName") == "ThankIntent":

                               

                                var2=req.get("result").get("parameters").get("number")

                                print("--------------------------------------------------------")

                                print(var2)

                                print("--------------------------------------------------------")

                                speech = "Thank you, your request is forwarded and you will receive the call soon from advisor."

                return {

                                "speech": speech,

                                "displayText": speech,

                                #"data": {},

                                # "contextOut": [],

                                "source": "apiai-onlinestore-shipping"

                }

 

 

 

 

if __name__ == '__main__':

                port = int(os.getenv('PORT', 5000))

 

                print ("Starting app on port %d" % port)

 

                app.run(debug=True, port=port, host='0.0.0.0')