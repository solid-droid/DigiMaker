from flask import *
import json
import pandas as pd

app = Flask(__name__)
#for claims by illness
def claimsby_illness(req):
    parameter_list = req.get('queryResult').get('parameters')
    print(parameter_list)
    disease =parameter_list.get('illness')
    message =open_file(1,disease,None)
    print ("request recieved")
    return message

#claims made by age min range and max range check if each parameter exists or not
def claimsby_age(req):
    parameter_list = req.get('queryResult').get('parameters')
    print(parameter_list)
    age =parameter_list.get('age')
    message =open_file(2,None,age)
    print ("request recieved")
    return message

# claims by gender no parameter with male and female  
# eg: 43 claims were made by males with total amount by ""
def claimsby_gender(req):
    parameter_list = req.get('queryResult').get('parameters')
    print(parameter_list)
    age =parameter_list.get('age')
    message =open_file(1,age)
    print ("request recieved")
    return message

#getting from the database
def open_file(para1,para2,para3):
    dataframe =""
    with open("team-techcrush/data/test_data.json") as datafile:
        data = json.load(datafile)
        dataframe = pd.DataFrame(data)
    cdf =dataframe.groupby("illness").count()
    count = 0
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
    return {'fulfillmentText': message}

#sample 
@app.route('/')
def hello_world():
    return 'Hello World TEST!'

@app.route('/reportMe',methods=['POST'])
def reportMe():
    return make_response(jsonify(results()))

if __name__ == '__main__':
    #  app.run() #For final run
    app.run(debug = True) #For debug only
