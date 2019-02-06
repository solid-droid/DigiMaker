from flask import *
import json
import pandas as pd
import module_illness
import module_reportgen
import module_gender
import module_age
import module_region

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
        module_reportgen.generate_report(req)
        message="Detailed report has been sent to your email successfully."
    elif str(intent_name) == "claimsby_gender" :
        message=module_gender.claimsby_gender(req)
    elif str(intent_name) == "claimsby_region" :
        message=module_region.claimsby_region(req)
    elif str(intent_name) == "claimsby_age" :
        message=module_age.claimsby_age(req)
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
