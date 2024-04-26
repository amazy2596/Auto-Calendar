from PIL import ImageGrab
from time import sleep
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from datetime import date
import pandas as pd
import pyautogui
import sqlite3
import requests
import webbrowser
import pytesseract
import re

def get_week_of_year(m, d, y):
    return date(y, m, d).isocalendar()[1]

def get_day_of_week(m, d, y):
    days_chinese = ["一", "二", "三", "四", "五", "六", "日"]
    return days_chinese[date(y, m, d).weekday()]

def parse_time(time):
    clean_time = time.strip()
    date_obj = datetime.strptime(clean_time, "%b/%d/%Y %H:%M")
    date_obj += timedelta(hours=5)
    time_str = date_obj.strftime("%H:%M")
    return date_obj.year, date_obj.month, date_obj.day, time_str

def operate_mouse(x, y, time, name):
    pyautogui.moveTo(x, y)
    pyautogui.click()
    pyautogui.click()
    sleep(1)
    pyautogui.typewrite(name)
    pyautogui.moveTo(1624, 919)
    sleep(1)
    pyautogui.click()
    pyautogui.moveTo(994, 881)
    sleep(1)
    pyautogui.click()
    pyautogui.typewrite(time)
    pyautogui.moveTo(994, 971)
    sleep(1)
    pyautogui.click()
    pyautogui.typewrite(time)
    pyautogui.moveTo(611, 583)
    sleep(1)
    pyautogui.click()

def auto_calendar(time, name):
    img_which_week = ImageGrab.grab(bbox=(600, 600, 650, 1900))
    img_which_day = ImageGrab.grab(bbox=(650, 600, 2500, 650))
    custom_config = r'--oem 3 --psm 6'

    text_data_week = pytesseract.image_to_data(img_which_week, output_type=pytesseract.Output.DATAFRAME, lang='chi_sim+eng', config=custom_config)
    text_data_day = pytesseract.image_to_data(img_which_day, output_type=pytesseract.Output.DATAFRAME, lang='chi_sim+eng', config=custom_config)

    pattern = r'\b([1-9]|[1-4][0-9]|5[0-3])\b'
    filtered_text = text_data_week[text_data_week['text'].astype(str).apply(lambda x: bool(re.search(pattern, x)))]
    filtered_text = filtered_text[['left', 'top', 'height', 'text']]
    week = filtered_text.to_dict(orient='records')

    year, m, d, time_str = parse_time(time)
    maxn, minn = 0, 0
    for i in week:
        maxn = max(maxn, int (i['text']))
        minn = min(minn, int (i['text']))
    if maxn < get_week_of_year(m, d, year):
        pyautogui.moveTo(972, 553)
        pyautogui.click()
    if minn > get_week_of_year(m, d, year):
        pyautogui.moveTo(892, 545)
        pyautogui.click()
    
    img_which_week = ImageGrab.grab(bbox=(600, 600, 650, 1900))
    text_data_week = pytesseract.image_to_data(img_which_week, output_type=pytesseract.Output.DATAFRAME, lang='chi_sim+eng', config=custom_config)

    pattern = r'\b([1-9]|[1-4][0-9]|5[0-3])\b'
    filtered_text = text_data_week[text_data_week['text'].astype(str).apply(lambda x: bool(re.search(pattern, x)))]
    filtered_text = filtered_text[['left', 'top', 'height', 'text']]
    week = filtered_text.to_dict(orient='records')

    for i in week:
        maxn = max(maxn, int (i['text']))
        minn = min(minn, int (i['text']))
    if maxn < get_week_of_year(m, d, year):
        pyautogui.moveTo(972, 553)
        pyautogui.click()
    if minn > get_week_of_year(m, d, year):
        pyautogui.moveTo(892, 545)
        pyautogui.click()
    
    img_which_week = ImageGrab.grab(bbox=(600, 600, 650, 1900))
    text_data_week = pytesseract.image_to_data(img_which_week, output_type=pytesseract.Output.DATAFRAME, lang='chi_sim+eng', config=custom_config)

    pattern = r'\b([1-9]|[1-4][0-9]|5[0-3])\b'
    filtered_text = text_data_week[text_data_week['text'].astype(str).apply(lambda x: bool(re.search(pattern, x)))]
    filtered_text = filtered_text[['left', 'top', 'height', 'text']]
    week = filtered_text.to_dict(orient='records')

    pattern = r'[一二三四五六日]'
    filtered_day = text_data_day[text_data_day['text'].astype(str).apply(lambda x: bool(re.search(pattern, x)))]
    filtered_day = filtered_day[['left', 'top', 'height', 'text']]
    day = filtered_day.to_dict(orient='records')
    
    for y in week:
        if int (y['text']) == get_week_of_year(m, d, year):
            for x in day:
                if x['text'] == get_day_of_week(m, d, year):
                    operate_mouse(int (x['left']) + 600, int (y['top']) + 600, time_str, name)

def check_contest_exist(name, time, webname):
    conn = sqlite3.connect(f'{webname}_contests.db')
    cursor = conn.cursor()
    cursor.execute(''' create table if not exists contests(
        time text,
        name text
    )''')
    cursor.execute("select * from contests where name = ?", (name,))
    result = cursor.fetchone()
    if not result:
        cursor.execute("insert into contests values(?, ?)", (time, name))
        conn.commit()
        auto_calendar(time, name)
    cursor.close()
    conn.close()

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
        check_contest_exist(name, time, 'codeforces')

def get_nowcoder_contest():
    url = "https://ac.nowcoder.com/acm/contest/vip-index"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    table = soup.find_all('table')[0]

url = "https://outlook.live.com/calendar/0/view/month"
webbrowser.open(url, autoraise = True)
get_codeforces_contest()