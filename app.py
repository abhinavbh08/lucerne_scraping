import psycopg2
from bs4 import BeautifulSoup
import requests
from utils import days_map

# Url of the page from which to fetch the data.
PAGE_URL = "https://www.lucernefestival.ch/en/program/summer-festival-22"

conn = psycopg2.connect(database="testdb", user = "postgres", password = "postgres", host = "db", port = "5432")
cur = conn.cursor()

# Creating the table
try:
    cur.execute("""CREATE TABLE data (
            id SERIAL PRIMARY KEY,
            title TEXT NOT NULL,
            date DATE NOT NULL,
            day TEXT NOT NULL,
            time TEXT NOT NULL, 
            location TEXT NOT NULL,
            artists TEXT,
            compositions TEXT,
            imageurl TEXT
        );""")
except:
    print("Cannot create the table")

conn.commit()

try:
    page = requests.get(PAGE_URL)
except:
    print("Could not read the page")


soup = BeautifulSoup(page.content, 'html.parser')

# Getting the events lists for the film festival.
event_div = soup.find("div",attrs={"class":"list","id":"event-list"})
events_list = event_div.find_all(class_="entry")

# Looping over and selecting the required things, and adding them to the database.
try:
    for index, event in enumerate(events_list):
        if index==0:
            continue
        day = days_map[event.select(".date-place .left .day")[0].get_text()]
        date = "2022-"+event.select(".date-place .left .month")[0].get_text()+"-"+ event.select(".date-place .left .date")[0].get_text()[:-1]
        time = event.select(".date-place .right .time")[0].get_text()
        location = event.select(".date-place .location")[0].get_text().replace("\n", "").replace("\t", "")
        url = event.select(".image")[0]["style"].split(" ")[1].replace("url(", "").replace(")", "")
        title = ", ".join(event.select(".event-info .surtitle")[0].get_text().split(" | "))
        artists = ", ".join(event.select(".event-info .title")[0].get_text().split(" | "))
        works = ", ".join(event.select(".event-info .subtitle")[0].get_text().split("\n")[1].replace("\n", "").replace("\t", "").split(" | "))
        insert_query = """INSERT 
        INTO data (title,date,day,time,location,artists,compositions,imageurl) 
        VALUES 
        (%s, %s, %s, %s, %s, %s, %s, %s);"""
        record_to_insert = (title, date, day, time, location, artists, works, url)
        cur.execute(insert_query, record_to_insert)
        conn.commit()    
except:
    print("Unable to insert elements in the database.")
finally:
    print("Inserted the data into the table.")
    conn.close()
    cur.close()
