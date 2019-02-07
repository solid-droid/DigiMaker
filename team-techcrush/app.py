from flask import *
import json
import pandas as pd
import module_illness
import module_gender
import module_age
import module_region
import module_testreport

app = Flask(__name__)

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
        if t == 0:
            message="Data for this state is currently unavailable"
        else:
            message="Detailed report has been sent to your email successfully."
    elif str(intent_name) == "claimsby_gender" :
        message=module_gender.claimsby_gender(req) 
    elif str(intent_name) == "claimsby_region" :
        message=module_region.claimsby_region(req) #pending
    elif str(intent_name) == "claimsby_age" :
        message=module_age.claimsby_age(req) #pending
    return {'fulfillmentText': message}

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
