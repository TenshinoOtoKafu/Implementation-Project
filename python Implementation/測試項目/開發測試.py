from unicodedata import normalize
import requests
import keyboard
import threading
import time

session = requests.Session()
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"}

url = ""
filterdomains=["google.com","bing.com","youtube.com","facebook.com","line.me","sharepoint.com","taobao.com","shopee.tw"]

# if data.url == url:
    # print("錯誤的")