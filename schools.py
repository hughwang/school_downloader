from urllib.request import urlopen
import re

# importing the csv module
import csv

# my data rows as dictionary objects


# field names
fields = ['id','school', 'principal', 'email', 'grades','type','url','address','city','zip','web','phone']

# name of csv file
filename = "ny_schools_Q.csv"
mydict=[]

for i in range(1,999):
    url = f"https://www.schools.nyc.gov/schools/Q{i:03}"
    try:
        page = urlopen(url)
        html_bytes = page.read()
        html = html_bytes.decode("utf-8")

        pattern = r'<a href="mailto:(.*)">(.*),(.*)Principal<\/a>'
        pattern_grades = r'<strong>Grades:<\/strong> (.*)<\/span>'
        pattern_school = r'<h1 class="title">(.*)</h1>'
        pattern_address = r'<a href="https:\/\/maps.google.com(.*)" target="_blank" class="more">(.*), (.*), NY (\d\d\d\d\d)<\/a>'
        pattern_web = r'<a href="(.*)" class="more">School Website<\/a>'
        pattern_phone = r'<span class="visually-hidden">Phone:<\/span>'

        lines = html.split('\n')
        principal = ''
        email = ''
        grades=''
        type=''
        address  =''
        city  =''
        zip  =''
        web = ''
        phone = ''
        loop_count=0
        for line in lines:
            match_results = re.search(pattern, line, re.IGNORECASE)
            if match_results:
                email = match_results.groups(0)[0]
                principal = match_results.groups(0)[1]
            match_results = re.search(pattern_address, line, re.IGNORECASE)
            if match_results:
                address = match_results.groups(0)[1]
                city = match_results.groups(0)[2]
                zip = match_results.groups(0)[3]
            match_results = re.search(pattern_grades, line, re.IGNORECASE)
            if match_results:
                grades = match_results.groups(0)[0]

                if ',10' in grades:
                    type = 'high'
                elif ',08' in grades:
                    type = 'middle'
                elif ',04' in grades:
                    type = 'elementary'
            match_results = re.search(pattern_school, line, re.IGNORECASE)
            if match_results:
                school = match_results.groups(0)[0]
            match_results = re.search(pattern_web, line, re.IGNORECASE)
            if match_results:
                web = match_results.groups(0)[0]
            match_results = re.search(pattern_phone, line, re.IGNORECASE)
            if match_results:
                phone = lines[loop_count+1]
                phone = phone.strip().replace('<span>','').replace('</span>','')
            loop_count = loop_count+1
        mydict.append({'id':f'{i:03}','school':school, 'principal':principal,
                       'email':email, 'grades':grades,'type':type,'url':url,
                       'address': address, 'city': city, 'zip': zip,
                       'web': web, 'phone': phone,

                       })
    except:
        pass

# writing to csv file
with open(filename, 'w') as csvfile:
    # creating a csv dict writer object
    writer = csv.DictWriter(csvfile, fieldnames=fields)

    # writing headers (field names)
    writer.writeheader()

    # writing data rows
    writer.writerows(mydict)