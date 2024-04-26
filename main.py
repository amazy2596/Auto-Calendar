from PIL import ImageGrab
from time import sleep
from io import StringIO
from bs4 import BeautifulSoup
import pandas as pd
import json
import sqlite3
import requests
import webbrowser
import pytesseract
import re

class Task: 
    def __init__(self, time, name):
        self.time = time
        self.name = name
    def build(self):
        return Task(self.time, self.name)

def get_which_day(y, m, d):
    if m == 1 or m ==2:
        m += 12
        y -= 1
    day = (d+2*m+3*(m+1)//5 + y + y//4 -y //100 + y//400 + 1) % 7
    return day

def auto_calendar():
    url = "https://outlook.live.com/calendar/0/view/month"
    webbrowser.open(url, autoraise = True)
    sleep(3)
    # img_which_week = ImageGrab.grab(bbox=(600, 600, 650, 1900))
    img_which_week = "week.png"
    custom_config = r'--oem 3 --psm 6'

    text_data_week = pytesseract.image_to_data(img_which_week, output_type=pytesseract.Output.DATAFRAME, lang='chi_sim+eng', config=custom_config)

    pattern = r'\b([1-9]|[1-4][0-9]|5[0-3])\b'
    filtered_text = text_data_week[text_data_week['text'].astype(str).apply(lambda x: bool(re.search(pattern, x)))]
    filtered_text = filtered_text[['left', 'top', 'height', 'text']]

    data = filtered_text.to_dict(orient='records')

    with open('week,json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def get_codeforces_contest():
    url = "https://codeforces.com/contests"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    table = soup.find_all('table')[0]
    rows = table.find_all('tr')
    contests = []
    for row in rows[1:]:
        cols = row.find_all('td')
        time = cols[2].get_text()
        name = cols[0].get_text()
        contests.append(Task(time, name).build())
    print(contests)
    return contests

codeforces_contests = sqlite3.connect('codeforces_contests.db')

cursor = codeforces_contests.cursor()

cursor.execute('''
               CREATE TABLE IF NOT EXISTS contests(
    time TEXT,
    name TEXT
)
''')

cursor.execute("insert into contests values('2021-09-25 15:35:00', 'Codeforces Round #744 (Div. 3)')")

codeforces_contests.commit()

cursor.execute('select * from contests')
rows = cursor.fetchall()
if rows:
    for row in rows:
        print(row)
else:
    print('No data')

cursor.close()
codeforces_contests.close()