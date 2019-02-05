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
#static data for makeGraph function
labels = 'Frogs', 'Hogs', 'Dogs', 'Logs'
sizes = [15, 30, 40, 15]
type="pie"

#function for Graph Generation
def makeGraph(x,y,type="pie"): 
    if type=="pie":
        f, ax1 = plt.subplots()
        ax1.pie(y, labels=x, autopct='%1.1f%%',shadow=True, startangle=90)
        ax1.axis('equal')
        #pdf filename
        filename ="sample.pdf"
        f.savefig(filename, bbox_inches='tight')


#function for email generation
def email_out():
    # html to include in the body section
    makeGraph(labels,sizes,type)
    html = """

    Dear, 

    This is the graph report.


    Best Regards,"""

    # Creating message.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Final report"
    msg['From'] = "teamcrush@gmail.com"
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
    server.login('techcrush31@gmail.com','techcrush123')
    server.sendmail(msg['From'], msg['To'], msg.as_string())
    server.quit()
    return{}




#for claims by illness
def claimsby_illness(req):
    parameter_list = req.get('queryResult').get('parameters')
    print(parameter_list)
    disease =parameter_list.get('illness')
    message =open_file(1,disease,None)
    print ("request recieved")
    return message

#claims made by age min range and max range check if each parameter exists or not
def claimsby_age(req):
    parameter_list = req.get('queryResult').get('parameters')
    print(parameter_list)
    age =parameter_list.get('age')
    message =open_file(2,None,age)
    print ("request recieved")
    return message

# claims by gender no parameter with male and female  
# eg: 43 claims were made by males with total amount by ""
def claimsby_gender(req):
    parameter_list = req.get('queryResult').get('parameters')
    print(parameter_list)
    age =parameter_list.get('age')
    message =open_file(1,age)
    print ("request recieved")
    return message

#function for email
def generate_report(req):
    parameter_list = req.get('queryResult').get('parameters')
    print(parameter_list)
    state =parameter_list.get('geo-state')

    message ="Detailed report has been sent to your email successfully."
    # print ("request recieved")
    return message


#getting from the database
def open_file(para1,para2,para3):
    dataframe =""
    with open("team-techcrush/data/test_data.json") as datafile:
        data = json.load(datafile)
        dataframe = pd.DataFrame(data)
    cdf =dataframe.groupby("illness").count()
    count = 0
    if para1 == 1:
       return "The number of people who have claimed for the illness is "+str(cdf.loc[para2,'id'])
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
        email_out()
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
