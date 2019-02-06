#Module for claims made by age min range and max range check if each parameter exists or not
def claimsby_age(req):
    parameter_list = req.get('queryResult').get('parameters')
    print(parameter_list)
    age =parameter_list.get('age')
    message =open_file(2,age)
    print ("request recieved")
    return message
