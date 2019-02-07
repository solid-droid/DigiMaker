#Module for status 
import json
import pandas as pd
def claimsby_region(req):
    count=""
    parameter_list = req.get('queryResult').get('parameters')
    # print(parameter_list)
    state =parameter_list.get('geo-state')
    with open("team-techcrush/data/test_data.json") as datafile:
        data = json.load(datafile)
        dataframe = pd.DataFrame(data)
        adf = dataframe[dataframe['status'] == 'approved'].agg({'id':['count']})
        rdf = dataframe[dataframe['status'] == 'rejected'].agg({'id':['count']})
        tdf = dataframe[dataframe['status'] == 'pending'].agg({'id':['count']})
        count_a=str(adf.loc['count','id'])
        count_r=str(rdf.loc['count','id'])
        count_p=str(tdf.loc['count','id'])
    return "There are "+count_a+" approved claims. "+count_p+" pending claims and "+count_r+" rejected claims as of today."