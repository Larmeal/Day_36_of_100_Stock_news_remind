from numpy import percentile
import requests
from twilio.rest import Client
import datetime as dt

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

now = dt.datetime.now()
data_delay = now.day - 4


## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
api_key_alphavantage = "RZZJPFVNTUROOVD2"
web_site_alphavantage = "https://www.alphavantage.co/query"
document_tsla_symbol = {
    "function": "TIME_SERIES_INTRADAY",
    "symbol": STOCK,
    "interval": "60min",
    "apikey": api_key_alphavantage
}

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
response_tsle = requests.get(web_site_alphavantage, params=document_tsla_symbol)
data_tsle = response_tsle.json()

open_price = float(data_tsle["Time Series (60min)"][f"2022-02-{data_delay} 05:00:00"]["1. open"])
close_price = float(data_tsle["Time Series (60min)"][f"2022-02-{data_delay} 20:00:00"]["4. close"])
percent_tsle = round((((close_price - open_price) / open_price) * 100), 2)
different_price_intraday = ""

if percent_tsle > 0:
    different_price_intraday = f"{STOCK} ▲ {percent_tsle}%"
else:
    different_price_intraday = f"{STOCK} ▼ {abs(percent_tsle)}%"


## STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME. 

api_key_newsapi = "c38da7905a1340dfb5694aa9cec72f03"
web_site_newsapi = 'https://newsapi.org/v2/everything'
document_tsla_info = {
       "q": COMPANY_NAME,
       "from": "2022-02-22",
       "sortBy": "popularity",
       "apiKey": api_key_newsapi
}

response_info = requests.get(web_site_newsapi, params=document_tsla_info)
data_info = response_info.json()

description_info = data_info["articles"][:3]
report_today = [index["description"] for index in description_info]


## STEP 3: Use https://www.twilio.com
# Send a separate message with the percentage change and each article's title and description to your phone number. 

account_sid = "AC4c525788499cf21ebc1db315cfb429dc"
auth_token = "93c5d06f9acb83fa5149b402cab4cd38"

client = Client(account_sid, auth_token)

for article in report_today:
    message = client.messages \
                    .create(
                        body=f"""{different_price_intraday}

    Headline: Were Hedge Funds Right About Piling Into Tesla Inc. {STOCK}?.

    Brief: {article}
                        """,
                        from_='+19034378260',
                        to='+66614385165'
                    )

    print(message.status)

