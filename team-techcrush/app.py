from flask import *
import json
import pandas as pd
import module_illness
import module_gender
import module_age
import module_region
import module_testreport
import module_status
import module_testcard


app = Flask(__name__)
dummyjson={
    "fulfillmentMessages": [
      {
        "platform": "ACTIONS_ON_GOOGLE",
        "simpleResponses": {
          "simpleResponses": [
            {
              "textToSpeech": "Report Analysis of Nebraska"
            }
          ]
        }
      },
      {
        "text": {
          "text": [
            "hello"
          ]
        }
      },
      {
        "platform": "ACTIONS_ON_GOOGLE",
        "card": {
          "image": {
            "imageUri": "https://3bd360be.ngrok.io/static/sample.png",
            
          }
        }
      }
    ]
}

#JSON request 
def results():
    message=""
    req = request.get_json(force=True)
    action = req.get('queryResult').get('action')
    intent_name = req.get('queryResult').get('intent').get('displayName')
    if str(intent_name) == "claimsby_illness":
        message =module_illness.claimsby_illness(req)  
    elif str(intent_name) == "generate_card":
          message= module_testcard.check_report(req)
          return dummyjson
    elif str(intent_name) == "generate_report":
        t=module_testreport.check_report(req)
        # print("*******************")
        print(str(t))
        if type(t) == None:
             message="Detailed report has been sent to your email successfully."
        elif t == 0 :
            message="Data for this state is currently unavailable"
        else:
            # print("*******************")
            # print(message+"#######")
            message="Detailed report has been sent to your email successfully."
    elif str(intent_name) == "claimsby_gender" :
        message=module_gender.claimsby_gender(req) 
    elif str(intent_name) == "claimsby_region" :
        message=module_region.claimsby_region(req)
    elif str(intent_name) == "claimsby_age" :
        message=module_age.claimsby_age(req) 
    elif str(intent_name) == "status" :
        message=module_status.claimsby_region(req)
    return {'fulfillmentText' : message}

#sample test for flask functionality
@app.route('/')
def hello_world():
    return 'Hello World TEST!'

#reportMe app functionality
@app.route('/reportMe',methods=['POST'])
def reportMe():
    return make_response(jsonify(results()))

path ="static/sample.png"
#reportMe app functionality
@app.route('/make_card')
def gen_card():
    return """<html><head></head><body><img src ="""+path+"""></body></html>"""

if __name__ == '__main__':
    #  app.run() #For final run
    app.run(debug = True) #For debug only
