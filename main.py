import requests
import selectorlib
import smtplib, ssl
import os
import time
import sqlite3



URL = "http://programmer100.pythonanywhere.com/tours"

connection = sqlite3.connect("data.db")
cursor = connection.cursor()

def scrape(url):
    """Scrape the page source from the url"""
    response = requests.get(url)
    source = response.text
    return source


def extract(source):
    extractor  = selectorlib.Extractor.from_yaml_file("extract.yaml")
    value = extractor.extract(source)["tours"]
    return value

    


def send_email(msg):
    host = "smtp.gmail.com"
    port = 465

    username = "atdbcoding@gmail.com"
    password = "nsmi exjc achx wlxi"

    receiver = "atdbcoding@gmail.com"
    context = ssl.create_default_context()

    msg = """\
Subject: New event found!
Hi we found a new event for you!
"""

    with smtplib.SMTP_SSL(host, port, context=context) as server:
        server.login(username, password)
        server.sendmail(username, receiver, msg)
    print("Email was sent!")

def store(extracted):
    row = extracted.split(",")
    row = [item.strip() for item in row ]
    cursor = connection.cursor()
    cursor.execute("INSERT INTO events VALUES(?,?,?)", row)
    connection.commit()
    
def read(extracted): 
    row = extracted.split(",")
    row = [item.strip() for item in row ]
    band, city, date = row
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM events WHERE band=? AND city=? AND date=?", (band, city, date))
    rows = cursor.fetchall()
    print(rows)
    return rows

if __name__ == "__main__":
        scraped = scrape(URL)
        extracted = extract(scraped)
        print(extracted)
        
        if extracted != "No upcoming tours":
            row = read(extracted)
            if not row:
                store(extracted)
                send_email(msg="")
time.sleep(2)