#Module for claims made by date
import json
import pandas as pd
from datetime import datetime as dt

def claimsby_date(option,date):
    message=""
    if option == 1:
        with open("team-techcrush/data/test_data.json") as datafile:
            data = json.load(datafile)
            dataframe = pd.DataFrame(data)
            t=dataframe
            s=dt.strptime(t.claimed_date, "%m/%d/%y")
            print(s)
            # print(type(t[['claimed_date']].to_datetime()))
            
    message="950 claims were submitted with a total amount of $43000 for $date."
    return message