#Module for claims made by age min range and max range check if each parameter exists or not
import json
import pandas as pd
def claimsby_region(req):
    count=""
    parameter_list = req.get('queryResult').get('parameters')
    print(parameter_list)
    state =parameter_list.get('geo-state')
    with open("team-techcrush/data/test_data.json") as datafile:
        data = json.load(datafile)
        dataframe = pd.DataFrame(data)
        cdf = dataframe[dataframe['state'] == state].agg({'id':['count']})
        count=str(cdf.loc['count','id'])
    return "There are "+count+" claims in "+state+"."