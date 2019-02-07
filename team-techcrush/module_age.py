#Module for claims made by age min range and max range check if each parameter exists or not
import json
import pandas as pd

def claimsby_age(req):
    parameter_list = req.get('queryResult').get('parameters')
    print(parameter_list)
    operation =parameter_list.get('oper')
    with open("team-techcrush/data/test_data.json") as datafile:
        data = json.load(datafile)
        dataframe = pd.DataFrame(data)
        t=dataframe
        if operation == "between":
            min_age =int(parameter_list.get('min_age'))
            max_age =int(parameter_list.get('max_age'))
            s =t[ (t['age']> min_age) & (t['age']< max_age)]['id'].count()
            c =t[ (t['age']> min_age) & (t['age']< max_age)]['claimed_amount'].astype('float64',copy=True,errors='raise')
            # print(c.sum())
    # with open("team-techcrush/data/test_data.json") as datafile:
    #     data = json.load(datafile)
    #     dataframe = pd.DataFrame(data)
    #     cdf = dataframe[dataframe['state'] == state].agg({'id':['count']})
    #     count=str(cdf.loc['count','id'])
    return "There are "+str(s)+" claims for the age group of "+str(min_age)+" and "+str(max_age)+" with a total amount of "+str(c.sum())+"."
