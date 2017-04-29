# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import logging
logging.basicConfig(level=logging.INFO,filename='c:/temp/log.txt')
from db import DB
import traceback

class Page():        
    def parse(self,url):
        r=requests.get(url)
        r.raise_for_status()
        html=r.text
        article=dict.fromkeys(['title','content'])
        #logging.info('/'*30)
        soup=BeautifulSoup(html,'html.parser')
        region=soup.find('section',attrs={'class':'article-grid__main'})
        text=region.find('div',attrs={'class':'article-text'})
        content=(text.div or text).get_text()
        if not content: logging.info(text)
        
        article['content']=content
        title=url.split('/')[-1] if url.split('/')[-1] else url.split('/')[-2]
        article['title']=title.replace('-',' ')
        return article

# class Pipeline():
    # def __init__(self):
        # self.open_spider()
        
    # def process_item(self, item):
        # #item=dict(item)
        # url=item.get('url')
        # logging.info(type(url))
        # content=item.get('content')[:30]
        # self.writer.writerow((url,))#,content
    # #需要保持的位置   
    # def open_spider(self):
        # self.f=open('article.csv','wb')
        # self.writer=csv.writer(self.f)
        # self.writer.writerow(('url','content'))
        
    # def close_spider(self):
        # self.f.close() 
            
if __name__=='__main__':
    page=Page()
    
    # pipe=Pipeline()
    # with open('item.csv','r')as f:
        # all=f.readlines()
        # #logging.info('/'*30)
        # for url in all:
            # url=url.strip().split(',')
            # if url[-2][:5]!='https':continue
            # logging.info(url[0])
            # #href:url[-2]
            # #logging.info(url[-2])
            # try:
                # article=page.parse(url[-2])
            # except:
                # logging.info(traceback.print_exc())
            # pipe.process_item(article)
        # pipe.close_spider()  
        
    dd=DB('contet.db')
    all = dd.queryDB('1')
    article=dict.fromkeys(['title','content'])
    for url in all:
        url=url[2]
        #print url
        try:
            article=page.parse(url)
        except:
            logging.info(traceback.print_exc())
        dd.insertDB(article)
    
    
    
    
    
    