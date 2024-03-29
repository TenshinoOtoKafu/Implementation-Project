from bs4 import BeautifulSoup
from lxml import etree
import requests
import httpx

"""
Todo    適用於 Python 3.10+

?   只寫個人常用的幾種 API 調用
"""

class CarryHead:
    # 使用 navigator.userAgent 直接獲取
    Head = {
        "Google": {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"},
        "Edge": {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0"}
    }

class Reques(CarryHead):
    def __init__(self, headers: str="Google", cookies: dict=None):
        """
        * headers: "Google" or "Edge", 兩字串擇一, 不處理例外
        * cookies: 傳入字典 cookie
        """
        self.session = requests.Session()
        self.headers = self.Head[headers]
        self.cookies = cookies

    # 解析要回傳的類型
    def __Parse(self, respon, type):
        return {
            "none" : respon,
            "text" : respon.text,
            "content" : respon.content,
            "status" : respon.status_code,
            "tree" : etree.HTML(respon.text),
            "bf" : BeautifulSoup(respon.text, "html.parser"),
        }[type]

    def get(self, url: str, type: str="text") -> any:
        """
        *   基本 Get 請求
        >>> [ url ]
        要請求的連結

        >>> [ type ]
        要獲取的結果類型
        ("none" / "text" / "content" / "status" / "tree" / "bf")

        "none" => 無處理
        "tree" => lxml 進行解析
        "bf" => bs4 進行解析
        """
        return self.__Parse(
            self.session.get(url, headers=self.headers, cookies=self.cookies),
            type
        )

    async def http_get(self, url: str) -> object:
        """
        *   異步 Get 請求

        >>> [ url ]
        要請求的連結

        >>> [ 使用方式 ]
        import asyncio
        async def main():
            work = [http_get(url) for url in date]
            results = await asyncio.gather(*work)
        asyncio.run(main())
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=self.headers, cookies=self.cookies)
            return etree.HTML(response.text)

    async def async_get(self, url: str, session) -> object:
        """
        *   異步 Get 請求

        >>> [ url ]
        要請求的連結

        >>> [ session ]
        請求的 session 值

        >>> [ 使用方式 ]
        import aiohttp
        async def main():
            async with aiohttp.ClientSession() as session:
                work = [async_get(url, session) for url in date]
                results = await asyncio.gather(*work)
        asyncio.run(main())
        """
        async with session.get(url, headers=self.headers, cookies=self.cookies) as response:
            content = await response.text()
            return etree.HTML(content)