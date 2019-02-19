from flask import *
import datetime
import dateutil
import json
import pandas as pd
import module_illness
import module_gender
import module_age
import module_region
import module_testreport
import module_status
import module_testcard
import module_date
import urllib.request

app = Flask(__name__)

def card_temp(req,cnt):
  parameter_list = req.get('queryResult').get('parameters')
      # print(parameter_list)
  state =parameter_list.get('geo-state')
  ngrokpath= "https://3941dcb4.ngrok.io/"
  print(cnt)
  filename="sample"+str(cnt)+".png"
  image= ngrokpath+"static/"+filename
  return {
          "fulfillmentMessages": [
        {
          "platform": "ACTIONS_ON_GOOGLE",
          "simpleResponses": {
            "simpleResponses": [
              {
                "textToSpeech": "Here you go, Analysis based on "+state+". Would you like me to send an email for it?"
              }
            ]
          }
        },
        {
          "text": {
            "text": [
              "Here you go, Analysis based on "+state+". Would you like me to send an email for it?"
            ]
          }
        },
        {
          "platform": "ACTIONS_ON_GOOGLE",
          "basicCard": {
            "image": {
              "imageUri": image,
              "accessibilityText": "Analysis based on "+state
            },
            "buttons": [
            {

              "title": "Show Image",
              "openUriAction": {
                "uri": image
              }
            }
          ]
          }
        }
      ]
  }

global cnt
cnt =1
#JSON request 
def results():
    global cnt
    print(cnt)
    message=""
    req = request.get_json(force=True)
    action = req.get('queryResult').get('action')
    intent_name = req.get('queryResult').get('intent').get('displayName')
    last_intent= intent_name
    if str(intent_name) == "claimsby_illness" or str(intent_name) == "claimsby_illness-followup":
        message =module_illness.claimsby_illness(req)  
    elif str(intent_name) == "generate_card-yes":
          module_testreport.check_report(req,1)
          message="Detailed report has been sent to your email successfully."
          return {'fulfillmentText' : message}
    elif str(intent_name) == "generate_card":
          message= module_testcard.check_report(req,cnt)
          # return dummyjson
          v= card_temp(req,cnt)
          cnt+=1
          return v
    elif str(intent_name) == "generate_report":
        t=module_testreport.check_report(req,0)
        # print("*******************")
        print(str(t))
        if type(t) == None or t == '' :
             message="Detailed report has been sent to your email successfully."
        elif t == 0 :
            message="Data for this state is currently unavailable"
            print("Unavilable : "+message)
        else:
            message="Detailed report has been sent to your email successfully."
        return {'fulfillmentText' : message}
    elif str(intent_name) == "claimsby_gender" :
        message=module_gender.claimsby_gender(req) 
    elif str(intent_name) == "claimsby_region" or str(intent_name) == "claimsby_region-followup":
        message=module_region.claimsby_region(req)
    elif str(intent_name) == "claimsby_age" :
        message=module_age.claimsby_age(req) 
    elif str(intent_name) == "status" :
        message=module_status.claimsby_region(req)
    elif str(intent_name) == "claimsby_date" :
        parameter_list = req.get('queryResult').get('parameters')
        print(parameter_list)
        if parameter_list['date'] == '' and parameter_list['fun-date'] !='' :
              print("******************")
              date_val =parameter_list['fun-date']
              if date_val == "today":
                    today = datetime.date.today()
                    message =module_date.claimsby_date(1,today,None)
                    return {'fulfillmentText' : message}
              elif date_val== "last date":
                    today = datetime.date.today()
                    yesterday = today - datetime.timedelta(days = 1)
                    message =module_date.claimsby_date(1,yesterday,None)
                    return {'fulfillmentText' : message}
              elif date_val== "last month":
                    message =module_date.claimsby_date(2,None,None)
                    return {'fulfillmentText' : message}
              elif date_val== "last 6 months":
                    message =module_date.claimsby_date(3,None,None)
                    return {'fulfillmentText' : message}
        elif parameter_list['date'] != '' and parameter_list['fun-date'] ==''  :
              print("###########")
              date_val= dateutil.parser.parse(parameter_list['date'], ignoretz=True)
              message=module_date.claimsby_date(1,date_val.date(),None)
        else:
              message= "Date Missing"
        # today = datetime.date.today()
        # yesterday = today - datetime.timedelta(days = 1)
        # print(today)
        # print(yesterday)
        # print(parameter_list['fun-date'])
        # # date_val =datetime.datetime.strptime(parameter_list['date'], '%Y-%m-%dT%H:%M:%S+%fZ')
        # print(type(date_val))
        # message = "date testing"
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
