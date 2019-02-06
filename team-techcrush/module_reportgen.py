#Module for report generation
import json
import pandas as pd
import matplotlib.pyplot as plt
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import email
import email.mime.application

#function for email
def generate_report(req):
    parameter_list = req.get('queryResult').get('parameters')
    # print(parameter_list)
    state =parameter_list.get('geo-state')
    open_file(2,state)
    email_out(state)
    # temp_x1 = dataframe.groupby(state)
    # print(temp_x1)
    # print ("request recieved")
    

def open_file(para1,para2):
    dataframe =""
    with open("team-techcrush/data/test_data.json") as datafile:
        data = json.load(datafile)
        dataframe = pd.DataFrame(data)
        t= dataframe
        cdf =t[t["state"] == para2].groupby("illness").count()
        df=t[t["state"] == para2]
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
            makeGraph(indexNames,indexValues,para2,"pie")
        # return "Detailed report has been sent to your email successfully."

#function for Graph Generation
def makeGraph(x,y,state,type="pie"): 
    if type=="pie":
        # plt.title ="Report Analysis of "+str(state)
        f, ax1 = plt.subplots()
        ax1.set_title("Report Analysis of "+str(state))
        ax1.pie(y, labels=x, autopct='%1.1f%%',shadow=True, startangle=90)
        ax1.axis('equal')
        plt.legend()
        #pdf filename
        filename ="sample.pdf"
        f.savefig(filename, bbox_inches='tight')

#function for email generation
def email_out(state):
    # html to include in the body section
    
    html = """
    
    Hi, <br><br>

        Report details has been attached in the mail based on """+str(state)+""".

    <br><br>
    <br>Thanks & Regards,
    <br>ReportMe
    """
    # Creating message.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Report Overview: "+str(state)
    msg['From'] = "reportme.analytics@gmail.com"
    msg['To'] = "glinzac@gmail.com"

    # The MIME types for text/html
    HTML_Contents = MIMEText(html, 'html')

    # Adding pptx file attachment
    filename = 'sample.pdf'
    fo = open(filename, 'rb')
    attach = email.mime.application.MIMEApplication(fo.read(), _subtype="ppt")
    fo.close()
    attach.add_header('Content-Disposition', 'attachment', filename=filename)

    # Attachment and HTML to body message.
    msg.attach(attach)
    msg.attach(HTML_Contents)

    # Your SMTP server information
    s_information = smtplib.SMTP()
    # You can also use SSL
    # smtplib.SMTP_SSL([host[, port[, local_hostname[, keyfile[, certfile[, timeout]]]]]])
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login('reportme.analytics@gmail.com','techrushhere')
    server.sendmail(msg['From'], msg['To'], msg.as_string())
    server.quit()
    return{}