#Module for report generation
import json
import pandas as pd
import matplotlib.pyplot as plt
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import email
import email.mime.application

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
    email_out(state)
    

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