
# Module for claims by gender no parameter with male and female  
# eg: 43 claims were made by males with total amount by ""
import json
import pandas as pd

def claimsby_gender(req):
    message =open_file(3,req)
    print ("request recieved")
    return message

def open_file(para1,para2):
    dataframe =""
    with open("team-techcrush/data/test_data.json") as datafile:
        data = json.load(datafile)
        dataframe = pd.DataFrame(data)
        t= dataframe
        cdf =t.groupby(["sex"]).count()
        mdf = t[t["sex"] == 'Male']['claimed_amount'].astype('float64',copy=True,errors='raise')
        # print(tdf)
        fdf = t[t["sex"] == 'Female']['claimed_amount'].astype('float64',copy=True,errors='raise')
        male =str(cdf.loc['Male','id'])
        female =str(cdf.loc['Female','id'])
        return male+" claims were submitted by males with a total claim amount of $"+str(int(mdf.sum()))+" and "+female+" claims by females with a total claim amount of $"+str(int(fdf.sum()))+"."