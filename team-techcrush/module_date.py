#Module for claims made by date
import json
import pandas as pd
from datetime import datetime as dt
from datetime import date as sysdt
from dateutil.relativedelta import *

def claimsby_date(option,dat,dat1):
    print(dat)
    print(type(dat))
    message=""
    count=0
    amt=0
    dataframe=""
    with open("team-techcrush/data/test_data1.json") as datafile:
            data = json.load(datafile)
            dataframe = pd.DataFrame(data)
    if option == 1:
        print("option 1")        
        t=dataframe
        for i in range(t['id'].count()):
            if pd.to_datetime(t['claimed_date'])[i].date() == dt.strptime(str(dat), "%Y-%m-%d").date() :
                count+=1
                curamt= float(t['claimed_amount'][i])
                amt+=curamt
    elif option == 2:
        print("option 2")
        t=dataframe
        today = sysdt.today()
        # last_mon =today-relativedelta(months=+1)
        compyr =today.year
        compmnth =today.month
        if compmnth == 2 :
            compyr=compyr-1
            compmnth=12
        else:
            compmnth=compmnth-2
        print(today.month-1)
        for i in range(t['id'].count()):
            if pd.to_datetime(t['claimed_date'])[i].year >= compyr and pd.to_datetime(t['claimed_date'])[i].month >= compmnth :
                count+=1
                curamt= float(t['claimed_amount'][i])
                amt+=curamt
    elif option == 3:
        print("option 3")
        t=dataframe
        today = sysdt.today()
        last_mon =today-relativedelta(months=+6)
        compyr=last_mon.year
        compmnth=last_mon.month
        # compyr =today.year
        # compmnth =today.month
        # compmnth=12-6+compmnth
        print(today.month-1)
        for i in range(t['id'].count()):
            if pd.to_datetime(t['claimed_date'])[i].year >= compyr and pd.to_datetime(t['claimed_date'])[i].month >= compmnth :
                count+=1
                curamt= float(t['claimed_amount'][i])
                amt+=curamt
    else:
        message="950 claims were submitted with a total amount of $43000 for $date."
    
    if count == 0:
        message= "No claims were made on "+str(dat)+"."
    elif count>0 and option ==1:
        message = str(count)+" claims were submitted with a total amount of $"+str(int(amt))+" for "+str(dat)+"."
    elif count>0 and option ==2:
        message = str(count)+" claims were submitted with a total amount of $"+str(int(amt))+" for last month."
    elif count>0 and option ==3:
        message = str(count)+" claims were submitted with a total amount of $"+str(int(amt))+" for last 6 months."
    return message
            # s= t[t['claimed_date'] == dat]
            # print(s)
        #     s=dt.strptime(t.claimed_date, "%m/%d/%y")
        #     print(s)

            # print(type(t[['claimed_date']].to_datetime()))
            # 1=>7
            # 2=>8
            # 3=>9
            # 4=>10
            # 5=>11
            # 6=>12
    
    return message