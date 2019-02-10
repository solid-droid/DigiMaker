import json
import pandas as pd
import module_reportgen

#Module for Testing Report Generation
def check_report(req,type):
    #type 0=> sample email gen 
    #type 1=> report gen for card.
    parameter_list=""
    if type ==0:
        parameter_list = req.get('queryResult').get('parameters')
    else:
        parameter_list=req.get('queryResult').get('outputContexts')[0].get('parameters')
    # print(parameter_list)
    state =parameter_list.get('geo-state')
    with open("team-techcrush/data/test_data.json") as datafile:
        data = json.load(datafile)
        dataframe = pd.DataFrame(data)
        cdf = dataframe[dataframe['state'] == state]
        print(cdf)
        if cdf.empty:
            return 0
        else:
            module_reportgen.workon_dataframe(cdf,state)
