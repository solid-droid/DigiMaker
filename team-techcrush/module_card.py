#Module for card generation
import json
import pandas as pd
import matplotlib.pyplot as plt
import os

def workon_dataframe(dataframe,state):
    cdf =dataframe.groupby("illness").count()
    df=dataframe
    # print(df['illness'].value_counts(normalize=True) * 100)
    print(type(cdf))
    indexNameArr =cdf.index.values
    indexNames = list(indexNameArr)
    indexValueArr =df['illness'].value_counts(normalize=True) * 100
    indexValues = list(indexValueArr)
    if(len(indexValues)< 0):
        print("File not found")
    else:
        print(indexValues)
        print(indexNames)
        makeGraph(indexNames,indexValues,state,"pie")

#function for Graph Generation
def makeGraph(x,y,state,type="pie"): 
    if type=="pie":
        # plt.title ="Report Analysis of "+str(state)
        f, ax1 = plt.subplots()
        # ax1.set_title("Report Analysis of "+str(state))
        ax1.pie(y, labels=x, autopct='%1.1f%%',shadow=True, startangle=90)
        ax1.axis('equal')
        plt.legend()
        #pdf filename
        filename ="sample.png"
        dirpath = os.getcwd()
        finalpath =dirpath+"\static\\"
        print(finalpath)
        f.savefig(filename, bbox_inches='tight')