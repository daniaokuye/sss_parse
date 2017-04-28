# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import csv
import logging
logging.basicConfig(level=logging.INFO,filename='log.txt')


class SssSpider():
    def __init__(self):
        self.url = 'https://www.scientificamerican.com/'
        self.html=self.downloader()
    def downloader(self):
        r=requests.get(self.url)
        r.raise_for_status()
        html=r.text
        return html
        
    def parse(self):
        colums={}
        soup=BeautifulSoup(self.html,'html.parser')
        article = soup.find_all('article')
        for item in article:
            colums.clear()
            #logging.info(item.article.attrs)
            title=item.attrs['data-listing-title']
            temp=item.attrs['data-listing-template']
            a=item.find_all('a')[0]
            href=a.attrs['href']
            tagDiv=item.find('div',class_='t_tag')
            text=tagDiv.string
            #logging.info(tagDiv)
            #logging.info(tagDiv.string)
            colums['title']=title
            colums['temp']=temp
            colums['href']=href
            colums['tag']=text
            #yield scrapy.Request(url=href,callback=Myspider2.parse)
            yield colums
            
if __name__ =='__main__':
    sss=SssSpider()
    with open('item.csv','wb') as f:
        writer=csv.writer(f)
        writer.writerow(('title','temp','href','tag'))    
        for item in sss.parse():
            #item=dict(item)
            title=item.get('title')
            temp=item.get('temp')
            href=item.get('href')
            tag=item.get('tag')
            writer.writerow((title,temp, href, tag))
        
        