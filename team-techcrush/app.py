from flask import *
import json
import pandas as pd

app = Flask(__name__)
#for claims by illness
def claimsby_illness(req):
    parameter_list = req.get('queryResult').get('parameters')
    print(parameter_list)
    disease =parameter_list.get('illness')
    message =open_file(1,disease)
    print ("request recieved")
    return message

def open_file(para1,para2):
    dataframe =""
    with open("team-techcrush/data/test_data.json") as datafile:
        data = json.load(datafile)
        dataframe = pd.DataFrame(data)
        # dataframe = pd.sum('')
    # print (dataframe.head(10))
    cdf =dataframe.groupby("illness").count()
    # print(cdf)
    # print(len(dataframe))
    count = 0
    # for i in range(len(dataframe)):
        # if dataframe(['ille'])
    # for i in range(len(data))
    if para1 == 1:
       return "The number of people who have claimed for the illness is "+str(cdf.loc[para2,'id'])
    return 'works!'

#JSON request 
def results():
    message=""
    req = request.get_json(force=True)
    action = req.get('queryResult').get('action')
    intent_name = req.get('queryResult').get('intent').get('displayName')
    if str(intent_name) == "claimsby_illness":
        message =claimsby_illness(req)  
    parameter_list = req.get('queryResult').get('parameters')
    print(parameter_list)
    # zone = req.get('queryResult').get('parameters').get('bank_name')
    # cost = {'Federal Bank':'6.85%', 'Allahabad Bank':'6.75%'}
    # speech = "The interest rate of " + zone + " is " + str(cost[zone])
    return {'fulfillmentText': message}

#sample 
@app.route('/')
def hello_world():
    # data = request.get_json(silent=True)
    return 'Hello World TEST!'

@app.route('/reportMe',methods=['POST'])
def reportMe():
    return make_response(jsonify(results()))

if __name__ == '__main__':
    #  app.run() #For final run
    app.run(debug = True) #For debug only
