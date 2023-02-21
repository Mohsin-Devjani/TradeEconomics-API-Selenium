import pandas as pd
import time 
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from selenium import webdriver 
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service


def get_trade_economics():
    Commodities = []
    date = datetime.now()
    formatdate = date.strftime("%Y-%m-%d %H:%M:%S")
    url = 'https://tradingeconomics.com/commodities'    
    chrome_options = Options()
    # To block notifications
    chrome_options.add_argument("--disable-notifications")
    driver = webdriver.Chrome(options=chrome_options)  
    # Market = ['Energy','Metals','Agricultural','Industrial','Livestock','Index','Electricity']
    driver.get(url)
    time.sleep(5)
    html = driver.page_source  
    soup = BeautifulSoup(html, "html.parser")
    indicers = soup.find_all('div', class_ = 'panel panel-default') 
    for i,dice in enumerate(indicers):
        Market = dice.find('th', class_ = 'te-sort').text.strip()
        info_wrapper = dice.find_all('tr', class_ = 'datatable-row')+(dice.find_all('tr',class_ = 'datatable-row-alternating'))
        for info in info_wrapper:
            Index = Market
            Name = info.find('td', class_='datatable-item-first').find('a').find('b').text.strip()
            Unit = info.find('td', class_='datatable-item-first').find('div').text.strip()
            Indicators = info.find_all('td','datatable-item')
            Price = Indicators[0].text.strip()
            Day = Indicators[1]['data-value']
            Percentage = Indicators[2]['data-value'] +'%'
            WeeklyTrend = Indicators[3]['data-value'] +'%'
            MonthlyTrend = Indicators[4]['data-value'] +'%'
            YoYTrend = Indicators[5]['data-value'] +'%'
            Date = formatdate
            Commodities.append({
                "Market": Index,
                "Name":Name,
                "Unit":Unit,
                "Price":Price,
                "Day":Day,
                "Percentage":Percentage,
                "WeeklyTrend":WeeklyTrend,
                "MonthlyTrend":MonthlyTrend,
                "YoYTrend":YoYTrend,
                "Date":Date
            })
    driver.close()
    tdate= date.strftime("%Y-%m-%d")
    file_name = f"TradeEconomics-{tdate}.csv"
    pd.DataFrame(Commodities).to_csv(file_name)



get_trade_economics()