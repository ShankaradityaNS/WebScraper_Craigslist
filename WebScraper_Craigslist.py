#Libraries Required#
import bs4
import pandas as pd
import requests
from bs4 import BeautifulSoup
#URL to be scraped#
url = "https://bangalore.craigslist.org/search/jjj?is_internship=1&is_nonprofit=1&is_telecommuting=1"
#Total number of jobs#
job_no = 0

#Creating a Directory#
d = {'key': 'value'}
print(d)

#Updating Directory#
d['new key'] = 'new value'
print(d)

npo_jobs = {}

while True:
 response = requests.get(url)   #Gets URL#
 data = response.text           #Gets data from URL#
 soup = BeautifulSoup(data,'html.parser')       #Converts data to html parser#
 tags = soup.find_all('a')                  #Finds all 'a' class data from soup#

 for tag in tags:
    tag.get('href')

 titles = soup.find_all("a",{"class":"result-title"})

 for title in titles:
    title.text              #Converts titlles to text#

 address = soup.find_all("span",{"class":"result-hood"})
 for addresses in address:
    addresses.text

 jobs = soup.find_all("p",{"class":"result-info"})

 for job in jobs:
   title = job.find("a",{"class":"result-title"}).text
   location_tag = job.find("span",{"class":"result-hood"})
   location = location_tag.text[2:-1] if location_tag else "N/A"
   date = job.find("time",{"class":"result-date"}).text
   link = job.find("a",{"class":"result-title"}).get('href')
   print("Title: "+title)
   print("Location: "+location)
   print("Starting Date: "+date)
   print("Link: "+link)
   job_no = job_no+1
   job_response = requests.get(link)
   job_data = job_response.text
   job_soup = BeautifulSoup(job_data,'html.parser')
   job_description = job_soup.find("section",{"id":"postingbody"}).text
   job_attributes_tag = job_soup.find("p",{"class":"attrgroup"})
   job_attributes = job_attributes_tag.text if job_attributes_tag else "N/A"
   print("Job Description: "+job_description)
   print("Job Attributes: "+job_attributes)
   npo_jobs[job_no] = [title, location, date, link, job_attributes, job_description]          #Structure of Directory#


 url_tag = soup.find('a',{"title":"next page"})             #Goes to next page#
 if url_tag.get('href'):
     url = "https://bangalore.craigslist.org/search/jjj?is_internship=1&is_nonprofit=1&is_telecommuting=1"+url_tag.get('href')
     print(url)
 else:
     break

print("Total No of Jobs: ", job_no)
npo_jobs_df = pd.DataFrame.from_dict(npo_jobs, orient='index', columns=['Job Title', 'Location', 'Date', 'Link', 'Job Attributes', 'Job Description'])
npo_jobs_df.to_csv('npo_jobs.csv')              #Updates data generated into a CSV File#