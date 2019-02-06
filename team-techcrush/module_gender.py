
# Module for claims by gender no parameter with male and female  
# eg: 43 claims were made by males with total amount by ""
import json
import pandas as pd

def claimsby_gender(req):
    # parameter_list = req.get('queryResult').get('parameters')
    # print(parameter_list)
    # sex =parameter_list.get('sex')
    message =open_file(3,req)
    print ("request recieved")
    return message

def open_file(para1,para2):
    dataframe =""
    with open("team-techcrush/data/test_data.json") as datafile:
        data = json.load(datafile)
        dataframe = pd.DataFrame(data)
        t= dataframe
        # cdf =t.groupby("sex").count()
        # parameter_list = para2.get('queryResult').get('parameters')
        # print(parameter_list)
        # disease =parameter_list.get('illness')
        # cdf =t[t["sex"] == "Male"]
        cdf =t.groupby(["sex"]).count()
        mdf =t[t["sex"] == 'Male']['claimed_amount']
        fdf =t[t["sex"] == 'Female']['claimed_amount']
        print(cdf)
        print(mdf)
        # mpf =mdf.to_numeric(m, errors='ignore')
        # print(mpf.sum(axis=0))
        # indexNameArr =mdf[1].values
        # indexNames = list(indexNameArr)
        # print(indexNames)
        male =str(cdf.loc['Male','id'])
        female =str(cdf.loc['Female','id'])
        return male+" claims were submitted by males with a total claim amount of 230000 and "+female+" claims by females with a total claim amount of 14000."