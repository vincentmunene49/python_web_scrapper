
from tokenize import String
import urllib.request
import urllib.parse
import urllib.error
from bs4 import BeautifulSoup
import ssl
import sqlite3
import time
from random import randint


class Webscrapping():
    """ 
    This class has three functions:
    readurl - checks whether there is an internet connection 
              then reads the url, in the specified time ie. after %sec or randomly if there is else notifies the user
    retrieve - retrieves the pages in the website,using beautiful soup lib,
               and iterates through every link in that page therefore the whole website

    dbconn - saves all the information obtained from the website in sqlite database.

    """

    def __init__(self, url, timeOption):
        self.url = url
        self.time = timeOption
        self.readurl(url)

    def readurl(self, url):
        # ignore ssl certificate errors
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

        try:
            html = urllib.request.urlopen(url, context=ctx).read()
        except Exception as err:
            print(f"Error: {err}")
            quit()

        self.soup = BeautifulSoup(html, 'html.parser')
        if self.time == 1:
            self.retrieveinfo()
            self.dbconn(url)
            time.sleep(5000)
        else:
            self.retrieveinfo()
            self.dbconn(url)
            time.sleep(randint(1000, 5000))

    def retrieveinfo(self):
        # Retrieve all the anchor tags and print the current url scrapping
        for link in self.soup.select('[href^=http]'):
            print(link.get('href'))
            url = link.get('href')
            self.readurl(url)

    def dbconn(self, url):
        # tblname = url.split('.')[1]
        conn = sqlite3.connect('Webcrawler.sqlite')
        cur = conn.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS tblinfo (Id INTEGER, links TEXT, Information TEXT,
             UNIQUE(links, Information))''')
        cur.execute('''
            INSERT OR IGNORE INTO tblinfo (links, information) VALUES (?, ?)''',
                    (url, self.soup.get_text()))


if __name__ == "__main__":
    choice = input(
        "Choose send type:\n1.Send request after every 5 minutes\n2.Send request randomly\nOption:")
    url: String = input("Enter url: ")
    if len(url.strip()) < 11:
        url = "https://maseno.ac.ke"
        print(f'Default Url: {url}')

    while True:
        if choice == 1:  # send the request after every 5 minutes
            Webscrapping(url, choice)
            time.sleep(5000)
        else:  # send the request randomly
            Webscrapping(url, choice)
            time.sleep(randint(1000, 5000))
