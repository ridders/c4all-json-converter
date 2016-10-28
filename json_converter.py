import time
import os
import json
from sys import argv

# Date & Time of When script is executed
date_time = (time.strftime(".%d%m%Y.%H%M%S"))

# The filename of the specified C4ALL Json file provided during execution
script, filename = argv

# Open the C4LL json file and loads the content for parsing
data_file = open(filename)
data = json.load(data_file)

print "*** C4ALL Version 1.1 JSON Converter *** \n"
print "Reading File: %s" % filename

# Seeks out the "Files" directory associated to the C4ALL file and renames it using the date_time variable 
full_path = os.path.abspath(filename).strip(filename)
os.rename(full_path + "files", full_path + "Files%s" % date_time)

# C4ALL json file case ID 
case_ID = data["value"][0]["odata.id"].replace('Case("', '').replace('")', '') 

# C4ALL json organisation information 
exhibit_ref = data["value"][0]["CaseNumber"]
organisation = data["value"][0]["ContactOrganization"]
contact_name =  data["value"][0]["ContactName"]
contact_number = data["value"][0]["ContactPhone"]
contact_email = data["value"][0]["ContactEmail"]
contact_title = data["value"][0]["ContactTitle"]

# Header for new json file
case_info = """{
  "odata.metadata":"http://github.com/ICMEC/ProjectVic/DataModels/1.1.xml#Cases","value":[
    {
      "odata.id":"Case(\\"%s\\")","Media@odata.navigationLinkUrl":"/Case(%s)/Media","Media":[\n        """

# Footer for new json file      
organisation_info = """\n      ],"CaseID":"%s","CaseNumber":"%s","ContactOrganization":"%s","ContactName":"","ContactPhone":"%s","ContactEmail":"%s","ContactTitle":"%s"
    }
  ]
}"""

def walk(mydict, key='value'):
    for row in mydict:
        for mediarow in row['Media']:
            yield [mediarow[key] for key in keylist if key in mediarow]

# Creates an empty json file and names it using the date_time variable
with open('Export%s.json' % date_time, 'wb') as f:

# Writes the json header to the new json file
    f.write(case_info % (case_ID, case_ID))

# Body of the new json file. Reads in required elements from original json and stores them in a list for printing
    keylist = ["MediaID", "MD5", "SHA1", "Name", "Category", "MediaSize", "RelativeFilePath"]

    file_info = []
    for item in walk(data.get('value')):
        dirpath = ('Files' + date_time)
        fname = item[6].split('.')
        
        file_info.append ("""{
          "odata.id":"Media(\\"%s\\")",
          "MediaID":%s,
          "MD5":"%s",
          "SHA1":"%s",
          "Name":"%s",
          "Category":%s,
          "MediaSize":"%s",
          "RelativeFilePath":"%s\\\%s.%s"
        }""" % (item[1], item[0], item[1], item[2], item[3].encode('ascii', 'ignore'), item[4], item[5], dirpath.encode('ascii', 'ignore'), item[1], fname[1]))
        
# Writes the json body to the new file
    f.write(','.join(file_info))

# Writes the json footer to the new file
    f.write(organisation_info % (case_ID, exhibit_ref, organisation, contact_number, contact_email, contact_title))
    
print('New JSON file created! Refer to: Export%s.json \n' % date_time)
print "Support: ridders57354@gmail.com"
