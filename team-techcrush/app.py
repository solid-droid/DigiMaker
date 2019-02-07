from flask import *
import json
import pandas as pd
import module_illness
import module_gender
import module_age
import module_region
import module_testreport
import module_status

app = Flask(__name__)
dummyjson={
    "fulfillmentMessages": [
      {
        "platform": "ACTIONS_ON_GOOGLE",
        "simpleResponses": {
          "simpleResponses": [
            {
              "textToSpeech": "hello karun"
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
        "basicCard": {
          "title": "Lulu Mall",
          "subtitle": "Edappally",
          "formattedText": "Lulu Mall Edappally",
          "image": {
            "imageUri": "https://www.tripsavvy.com/thmb/6q9juU2zfKFSygpLubTdr3UPC-g=/870x0/filters:no_upscale():max_bytes(150000):strip_icc():format(webp)/Union-Station-Map-3-575b02515f9b58f22ed75377.jpg",
            "accessibilityText": "i dont know"
          },
          "buttons": [
            {
              "title": "Open google map",
              "openUriAction": {
                "uri": "https://www.google.com/maps/dir/?api=1&query=lulu+mall+edappally"
              }
            }
          ]
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
    return dummyjson

#sample test for flask functionality
@app.route('/')
def hello_world():
    return 'Hello World TEST!'

#reportMe app functionality
@app.route('/reportMe',methods=['POST'])
def reportMe():
    return make_response(jsonify(results()))

if __name__ == '__main__':
    #  app.run() #For final run
    app.run(debug = True) #For debug only
