import csv 
    
# my data rows as dictionary objects 
'''
mydict =[{'branch': 'COE', 'cgpa': '9.0', 'name': 'Nikhil', 'year': '2'}, 
         {'branch': 'COE', 'cgpa': '9.1', 'name': 'Sanchit', 'year': '2'}, 
         {'branch': 'IT', 'cgpa': '9.3', 'name': 'Aditya', 'year': '2'}, 
         {'branch': 'SE', 'cgpa': '9.5', 'name': 'Sagar', 'year': '1'}, 
         {'branch': 'MCE', 'cgpa': '7.8', 'name': 'Prateek', 'year': '3'}, 
         {'branch': 'EP', 'cgpa': '9.1', 'name': 'Sahil', 'year': '2'}] 
'''    
mydict = [
          {'acckey':'ab216c0aefe0e39811304929a5cf0d8d','accnum':'301496'},
          {'acckey':'3d413007f995fdfb75f2931299cb9041','accnum':'301496'},
          {'acckey':'9dae43726fba08ab368257032e9b4b2b','accnum':'301496'},
          {'acckey':'1b526567f21042c34a424591652a8285','accnum':'301496'},

]
# field names 
fields = ['acckey', 'accnum']
    
# name of csv file 
filename = "university_records.csv"
    
# writing to csv file 
with open(filename, 'w') as csvfile: 
    # creating a csv dict writer object 
    writer = csv.DictWriter(csvfile, fieldnames = fields) 
        
    # writing headers (field names) 
    writer.writeheader() 
        
    # writing data rows 
    writer.writerows(mydict)
