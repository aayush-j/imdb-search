# This script scraps data of a movie from IMDB.
# Just enter name of your movie.
# Libraries used: urllib.request, os, BeautifulSoup, datetime.
# There are issues with some searches particularly tv series.

import urllib.request, os
from bs4 import BeautifulSoup
from datetime import date

print("Welcome to IMDB Search.")
search = str(input("What do you want to search? "))

# splits into separate strings to make our url
search_list = search.split()
url_config = ""

# preparating url
for text in search_list:
    url_config += text+"+"

url = "http://www.imdb.com/find?ref_=nv_sr_fn&q="+url_config+"&s=all"
# loading webpage
page = urllib.request.urlopen(url)
# parsing html
soup = BeautifulSoup(page, 'html.parser')

# retrieving url of first search result
content = soup.find('tr', {'class': 'findResult odd'})
# extracting url
main_url = 'http://www.imdb.com'+content.find('a')['href']
main_page = urllib.request.urlopen(main_url)

soup2 = BeautifulSoup(main_page, 'html.parser')
content2 = soup2.find('div', {'class': 'titleBar'})

# extracting different contents of a movie
# .strip() is used to remove spaces before and after the content
title = (content2.find('h1').text).strip()
rating = ((soup2.find('span', {'itemprop': 'ratingValue'})).text).strip()
release_date = ((content2.find('a', {'title': 'See more release dates'})).text).strip()
runtime = ((content2.find('time', {'itemprop': 'duration'})).text).strip()

content2 = soup2.find('div', {'id': 'titleStoryLine'})

storyline = ((content2.find('p')).text).strip()
certificate = (content2.find('span', {'itemprop': 'contentRating'})).text

# printing our data
print("Name: "+title)
print("Rating: "+rating+"/10")
print("Release Date: "+release_date)
print("Duration: "+runtime)
print("Synopsis: "+storyline)
print("Certification: "+certificate)

# saving our data into our database
choice = str(input("Do you want to save this in your database? Yes/No >>> "))
if choice.upper()=="YES":
# Note: opening file in append mode so that previous data is not deleted
# making a directory to store our file.
# first line checks if directory already exists
    if not os.path.exists('imdb'):
        os.makedirs('imdb')
    with open('imdb/imdb_database.txt', 'a') as file:
        file.write(str(date.today())+"\n")
        file.write("Name: "+title+"\n")
        file.write("Rating: "+rating+"/10\n")
        file.write("Release Date: "+release_date+"\n")
        file.write("Duration: "+runtime+"\n")
        file.write("Synopsis: "+storyline+"\n")
        file.write("Certification: "+certificate+"\n\n")



