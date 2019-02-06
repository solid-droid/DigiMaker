from flask import *
import json
import pandas as pd
#imports for email
import matplotlib.pyplot as plt
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import email
import email.mime.application

app = Flask(__name__)

#function for Graph Generation
#add headers for the graph
def makeGraph(x,y,state,type="pie"): 
    if type=="pie":
        # plt.title ="Report Analysis of "+str(state)
        f, ax1 = plt.subplots()
        ax1.set_title("Report Analysis of "+str(state))
        ax1.legend(x)
        ax1.pie(y, labels=x, autopct='%1.1f%%',shadow=True, startangle=90)
        ax1.axis('equal')
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
    msg['To'] = "techcrush31@gmail.com"

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




#for claims by illness
def claimsby_illness(req):
    parameter_list = req.get('queryResult').get('parameters')
    print(parameter_list)
    disease =parameter_list.get('illness')
    message =open_file(1,disease)
    print ("request recieved")
    return message

#claims made by age min range and max range check if each parameter exists or not
def claimsby_age(req):
    parameter_list = req.get('queryResult').get('parameters')
    print(parameter_list)
    age =parameter_list.get('age')
    message =open_file(2,age)
    print ("request recieved")
    return message

# claims by gender no parameter with male and female  
# eg: 43 claims were made by males with total amount by ""
# 43 claims were submitted by males with a total claim amount of 230000 and 28 claims by females with a total claim amount of 14000.
def claimsby_gender(req):
    parameter_list = req.get('queryResult').get('parameters')
    print(parameter_list)
    age =parameter_list.get('age')
    message =open_file(3,age)
    print ("request recieved")
    return message

#function for email
def generate_report(req):
    parameter_list = req.get('queryResult').get('parameters')
    # print(parameter_list)
    state =parameter_list.get('geo-state')
    message =open_file(2,state)
    email_out(state)
    # temp_x1 = dataframe.groupby(state)
    # print(temp_x1)
    # print ("request recieved")
    return message


#getting from the database
#para1 => illness
#para2 => Report Generation
def open_file(para1,para2):
    dataframe =""
    with open("team-techcrush/data/test_data.json") as datafile:
        data = json.load(datafile)
        dataframe = pd.DataFrame(data)
    if para1 == 1:
        cdf =dataframe.groupby("illness").count()
        return "The number of people who have claimed for the illness is "+str(cdf.loc[para2,'id'])+"."
    elif para1 == 2:
        t= dataframe
        cdf =t[t["state"] == para2].groupby("illness").count()
        df=t[t["state"] == para2]
        # print(df['illness'].value_counts(normalize=True) * 100)
        # print(cdf.head())
        indexNameArr =cdf.index.values
        indexNames = list(indexNameArr)
        indexValueArr =df['illness'].value_counts(normalize=True) * 100
        indexValues = list(indexValueArr)
        makeGraph(indexNames,indexValues,para2,"pie")
        print(indexValues)
        print(indexNames)
        return "Detailed report has been sent to your email successfully."
    elif para1 == 3:
        return "claims by gender working. "
    return 'works!'

#JSON request 
def results():
    message=""
    req = request.get_json(force=True)
    action = req.get('queryResult').get('action')
    intent_name = req.get('queryResult').get('intent').get('displayName')
    if str(intent_name) == "claimsby_illness":
        message =claimsby_illness(req)  
    elif str(intent_name) == "generate_report":
        message=generate_report(req)
    elif str(intent_name) == "claimsby_gender" :
        message=claimsby_gender(req)
    parameter_list = req.get('queryResult').get('parameters')
    print(parameter_list)
    return {'fulfillmentText': message}

#sample 
@app.route('/')
def hello_world():
    return 'Hello World TEST!'

@app.route('/reportMe',methods=['POST'])
def reportMe():
    return make_response(jsonify(results()))

if __name__ == '__main__':
    #  app.run() #For final run
    app.run(debug = True) #For debug only
