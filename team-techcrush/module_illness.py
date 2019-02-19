#Module for claims by illness
import json
import pandas as pd


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
        cdf = dataframe.groupby("illness").count()
        # return "The number of people who have claimed for the "+str(para2)+" is "+str(cdf.loc[para2,'id'])+"."
        return "There are "+  str(cdf.loc[para2,'id']) +" number of claims based on the illness, " + str(para2)+"."