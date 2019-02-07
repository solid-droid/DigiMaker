#Module for claims made by age min range and max range check if each parameter exists or not
import json
import pandas as pd

def claimsby_age(req):
    parameter_list = req.get('queryResult').get('parameters')
    print(parameter_list)
    operation =parameter_list.get('oper')
    message=""
    with open("team-techcrush/data/test_data.json") as datafile:
        data = json.load(datafile)
        dataframe = pd.DataFrame(data)
        t=dataframe
        print(operation)
        if operation == "between":
            min_age =int(parameter_list.get('min_age'))
            max_age =int(parameter_list.get('max_age'))
            s =t[ (t['age']> min_age) & (t['age']< max_age)]['id'].count()
            c =t[ (t['age']> min_age) & (t['age']< max_age)]['claimed_amount'].astype('float64',copy=True,errors='raise')
            message ="There are "+str(s)+" claims for the age "+operation+" of "+str(min_age)+" and "+str(max_age)+" with a total amount of $"+str(c.sum())+"."
        elif operation == "above":
            age =int(parameter_list.get('age')['amount'])
            s =t[ (t['age']> age)]['id'].count() 
            c =t[ (t['age']> age)]['claimed_amount'].astype('float64',copy=True,errors='raise')
            message="The number of claims is "+str(s)+" and the total claimed amount is $"+str(c.sum())+" for the age "+operation+" "+str(age)+"."
            # message ="The number of claims is "+str(s)+" for the age above "+str(age)+" and "+str(max_age)+" with a total amount of "+str(c.sum())+"."
        # elif operation == "below":
        #     age =int(parameter_list.get('age'))
        #     s =t[ (t['age']< age)]['id'].count()
        #     c =t[ (t['age']< age)]['claimed_amount'].astype('float64',copy=True,errors='raise')  
        #     message="The number of claims is "+str(s)+" and the total claimed amount is "+str(c.sum())+" for the age "+operation+" "+str(age)+"."  
            # print(c.sum())
    # with open("team-techcrush/data/test_data.json") as datafile:
    #     data = json.load(datafile)
    #     dataframe = pd.DataFrame(data)
    #     cdf = dataframe[dataframe['state'] == state].agg({'id':['count']})
    #     count=str(cdf.loc['count','id'])
    return message
