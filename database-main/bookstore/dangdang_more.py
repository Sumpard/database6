import asyncio
import json
import re
import sys
import pandas as pd
from fake_useragent import UserAgent
from parsel import Selector
import httpx

#
# print(df["详情页"])


class DangdangSpider:
    def __init__(self) -> None:
        self.ua = UserAgent()
        self.headers = {"User-Agent": self.ua.random}
        self.df = pd.read_csv("dangdang-new.csv").drop_duplicates()
        self.df.to_csv("dangdang-neww.csv", index=False)

    async def run(self, url: str):
        async with httpx.AsyncClient() as client:
            resp = await client.get(url, headers=self.headers)
            print(url, resp)
            S = Selector(resp.text)
            detail = S.css("ul.key.clearfix li::text").getall()
            category = []
            for lie in S.css("#detail-category-path .lie"):
                category.append(lie.css("a::text").getall())
            return detail, category

    async def work(self):

        # Python 3.6之前用ayncio.ensure_future或loop.create_task方法创建单个协程任务
        # Python 3.7以后可以用户asyncio.create_task方法创建单个协程任务
        tasks = [self.run(url) for url in self.df["详情页"][: 20]]

        # 还可以使用asyncio.gather(*tasks)命令将多个协程任务加入到事件循环
        results = await asyncio.gather(*tasks)
        print(results)
        results = [json.dumps(a) for a in results]
        print(results)
        # self.df.insert(len(self.df.columns), "details", results)
        # self.df.to_csv("dangdang.csv", index=False)


spider = DangdangSpider()
print([re.search(r"/(\d+)\.html", s).group(1) for s in spider.df["详情页"].tolist()])
# asyncio.run(spider.work())
