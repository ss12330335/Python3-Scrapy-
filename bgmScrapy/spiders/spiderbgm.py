# -*- coding: utf-8-sig -*-
import scrapy
import re
import csv
from bgmScrapy.items import BangumiItem

class SpiderbgmSpider(scrapy.Spider):
    name = 'bangumiScrapy'
    #start_urls = ['https://bgm.tv/anime/browser?sort=rank']
    headers = {}

    def start_requests(self):
        url = 'https://bgm.tv/anime/browser?sort=rank'
        yield scrapy.Request(url, headers=self.headers)

    def parse(self, response):
        item = BangumiItem()
        moives = response.xpath("//ul[@id='browserItemList']")
        for moive in moives:
            moiveDetail = moive.xpath(".//li/div[@class='inner']")
            item["ranking"] = moiveDetail.xpath(".//span[@class='rank']/text()").extract()
            item["name"] = moiveDetail.xpath(".//h3/a/text()").extract()
            eps, ts, sts = [], [], []
            for i in moiveDetail.xpath(".//p[@class='info tip']/text()").extract():
                #if re.search(r"\d+话", i):
                #    eps.append(re.search(r"\d+话", i)[0])
                #else:
                #    eps.append("")
                #ts.append(re.search(r"(\d+年\d+月\d+日)|(\d+年\d+月)|(\d+年)", i)[0])
                #sts.append(str(i)[re.search(r"(\d+年\d+月\d+日)|(\d+年\d+月)|(\d+年)",
                #                          i).span()[1]+3:len(str(i))])
                arr = str(i).split('/')
                staffPos = -1
                staff = ""
                assert(len(arr) > 0)
                if re.search(r"\d+话", arr[0]):
                    eps.append(arr[0][1:len(arr[0])])
                    ts.append(arr[1])
                    staffPos = 2
                else:
                    eps.append("")
                    ts.append(arr[0][1:len(arr[0])])
                    staffPos = 1
                for n in range(staffPos, len(arr)):
                    staff += (arr[n] + "、")
                sts.append(staff)
            item["episodes"] = eps
            item["time"] = ts
            item["staffs"] = sts
            item["score"] = moiveDetail.xpath(".//p[@class='rateInfo']/small/text()").extract()
            item["voteNum"] = moiveDetail.xpath(".//p[@class='rateInfo']/span[@class='tip_j']/text()").\
                re(r"[(](\d+人)评分[)]")
            #for i in zip(item["ranking"], item["name"], item["episodes"], item["time"],
            #             item["staffs"], item["score"], item["voteNum"]):
            #    print(i)
            with open("bangumiScrapyOutput.csv", "a+", newline='', encoding="utf-8-sig") as fp:
                res = list(zip(item["ranking"], item["name"], item["episodes"], item["time"],
                               item["staffs"], item["score"], item["voteNum"]))
                writer = csv.writer(fp)
                for i in range(len(res)):
                    writer.writerow(list(res[i]))

        nextUrl = response.xpath("//div[@class='section']/div[@class='clearit']/"
                                 "div[@class='page_inner']/a[text()='››']/@href").extract()
        print("nextUrl = " + str(nextUrl))
        print("https://bgm.tv/anime/browser?sort=rank" + nextUrl[0][10:len(nextUrl[0])])
        if nextUrl:
            yield scrapy.Request("https://bgm.tv/anime/browser?sort=rank"
                           + nextUrl[0][10:len(nextUrl[0])])
