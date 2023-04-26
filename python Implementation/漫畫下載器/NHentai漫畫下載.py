from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
from lxml import etree
from tqdm import tqdm
import cloudscraper
import threading
import requests
import random
import time
import re
import os
dir = os.path.abspath("R:/") # 可更改預設路徑
os.chdir(dir)
# 漫畫主頁處理
class Verify:
    def __init__(self,enter,pages):
        self.search = r"https://nhentai\.net/.*"
        self.mangapage = r"https://nhentai\.net/g/\d+"
        self.correctbox = []
        self.pages = pages

        if isinstance(enter,list):
            # 將錯誤的網址格式排除
            for data in enter:
                if re.match(self.mangapage,data):
                    self.correctbox.append(data)
                else:pass

            # 將正確的網址導入請求
            if len(self.correctbox) != 0:
                for run in self.correctbox:self.run(run)
            else:pass

        else:
            # 將匹配的單條網址,傳入陣列,並導入請求
            if re.match(self.mangapage,enter):
                self.correctbox.append(enter)
                self.run(self.correctbox)
            elif re.match(self.search,enter):
                if enter.find("?page") != -1:url = f"{enter.split('?page=')[0]}?page=1"
                else:url = f"{enter}?page=1"
                
                for page in range(1,self.pages+1):
                    print(f"{url.split('?page=')[0]}?page={page}")
                # 待更新...
            else:pass

    # 開始請求
    def run(self,url):
        for deal in url:download.Data_Request(deal)
class ComicsHomePage:
    def __init__(self,delay=7,head=True):
        self.head = head    # 判斷是否隱藏窗口
        self.Delay = delay  # 延遲處理
        self.title = ""     # 漫畫名稱
        self.labelbox = {}  # 保存標籤數據
        self.Home = None    # 主頁Html存放
        self.SaveNameFormat = 1
        self.headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"}

    def add(self):
        Settings = uc.ChromeOptions()
        if self.head:Settings.add_argument("--headless")
        Settings.add_argument(f"--remote-debugging-port={random.randint(1024,65535)}")
        Settings.add_argument('--user-data-dir=R:/')
        Settings.add_argument('--no-first-run --no-service-autorun --password-store=basic')
        return Settings
    
    def enter(self,Url,pages=None,delay=None,head=None):
        if delay != None:self.Delay = delay
        if head != None:self.Title = head 
        Verify(Url,pages)
    
    def Data_Request(self,Url):
        browser = uc.Chrome(self.add())
        # 開啟漫畫主頁
        browser.get(Url)

        try: # 測試點選機器人認證
            human = WebDriverWait(browser,30).until(EC.element_to_be_clickable((By.XPATH, "//input[@type='checkbox']")))
            browser.execute_script("arguments[0].click();",human)
        except:pass

        time.sleep(self.Delay)
        # 取得主頁代碼,並呼叫處理
        self.Home = etree.fromstring(browser.page_source,etree.HTMLParser())
        self.Data_Processing()

        # 處理完成後,獲取總共頁數,和創建資料夾
        Pages = self.labelbox['Pages'][0]
        self.Folder_Creation(self.title)

        print(f"{self.title}\n開始下載 ==>")
        # 創建進度條
        pbar = tqdm(total=int(Pages))
        
        for page in range(1,int(Pages)+1):
            browser.get(f"{Url}/{page}/")
            ImgUrl = etree.fromstring(browser.page_source,etree.HTMLParser()).xpath("//section[@id='image-container']/a/img")[0].get('src')
            
            if int(Pages) >= 100:SaveName = f"{self.SaveNameFormat:03d}.{ImgUrl.split('.')[-1]}"
            else:SaveName = f"{self.SaveNameFormat:02d}.{ImgUrl.split('.')[-1]}"

            threading.Thread(target=self.Download,args=(os.path.join(dir,self.title),SaveName,ImgUrl,self.headers)).start()
            
            self.SaveNameFormat += 1
            pbar.update(1)

        pbar.close()
        browser.quit()

    # 處理主頁數據
    def Data_Processing(self):
        try:
            title = self.Home.xpath("//h2[@class='title']")[0]
            self.title = re.sub(r'[<>:"/\\|?*]', '', "".join(title.xpath(".//text()")).strip())
            
            labelbox = self.Home.xpath("//section[@id='tags']")[0]
            for index , tag in enumerate(labelbox.xpath(".//div")):
                if index == 4 or index == 6 or index == 8:continue # 這邊是排除不需要的數據
                else:self.labelbox[tag.text.strip().rstrip(':')] = tag.xpath(".//span[@class='name']/text()")
        except:
            print("請嘗試將ComicsHomePage,第三參數設置為False\n或者再次運行")
            os._exit(0)

        # self.labelbox 大致格式
        # {'Parodies': [''], 'Characters': ['', ''], 'Tags': [''], 'Artists': [''], 'Languages': ['', ''], 'Pages': ['']}

    # 創建資料夾
    def Folder_Creation(self,FolderName):
        try:
            os.mkdir(FolderName)
        except:
            pass

    # 下載圖片
    def Download(self,location,picturename,imageurl,headers):

        ImageData = requests.get(imageurl, headers=headers)
        if ImageData.status_code == 200:
            with open(os.path.join(location,picturename),"wb") as f:
                f.write(ImageData.content)
download = ComicsHomePage()
"""
該網站的反爬機制,無法使用免費版的cloudscraper進行繞過,因此使用自動化操作
有時候跳出的是,機器人驗證的部份,目前無解決相關問題,所以可以再次運行試試

製作想法:
批量下載
搜尋頁面下載
同名分類與排除
tag標籤排除
"""
if __name__ == "__main__":  
    Batch_Box = []

    # url,頁數,延遲,隱藏窗口
    download.enter("https://nhentai.net/character/kuroyukihime/",10,3)