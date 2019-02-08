import json
import pandas as pd
import module_card

def check_report(req):
    parameter_list = req.get('queryResult').get('parameters')
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
            module_card.workon_dataframe(cdf,state)
