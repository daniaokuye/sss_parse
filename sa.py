# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import logging
logging.basicConfig(level=logging.INFO,filename='c:/temp/log.txt')
from db import DB
from pg import Page
import traceback

#clouds denpency
from scipy.misc import imread
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

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
            #print title
            temp=item.attrs['data-listing-template']
            a=item.find_all('a')[0]
            href=a.attrs['href']
            tagDiv=item.find('div',class_='t_tag')
            text=tagDiv.string
            #logging.info(tagDiv)
            #logging.info(tagDiv.string)
            title=href.split('/')[-1] if href.split('/')[-1] else href.split('/')[-2]
            colums['title']=title.replace('-',' ')
            colums['temp']=temp
            colums['href']=href
            colums['tag']=text
            #yield scrapy.Request(url=href,callback=Myspider2.parse)
            yield colums
            
            
            
class WordC:
    def __init__(self):
        self.cloud()
        
    def cloud(self):    
        dd=DB('contet.db')
        all = dd.queryDB('1')
        words=''
        for text in all:
            if text[-1]:text=text[-1].encode('utf-8')
            else: continue
            words+=text
        back_coloring = imread("chun_li.jpg")
        wc = WordCloud(background_color="white", #背景颜色  
                        max_words=2000,# 词云显示的最大词数  
                        mask=back_coloring,#设置背景图片  
                        max_font_size=100, #字体最大值  
                        random_state=42
                        #font_path='./font/cabin-sketch.bold.ttf',#设置字体         
                        )  
        wc.generate(words)
        image_colors = ImageColorGenerator(back_coloring)  
        plt.figure()  
        # 以下代码显示图片  
        plt.imshow(wc)  
        plt.axis("off")  
        plt.show()

        
if __name__ =='__main__':
    sss=SssSpider()
       
    dd=DB('contet.db')
    for item in sss.parse():    
        dd.insertDB(item)  
    dd.closeDB()    
    
    #carry out page
    page=Page()   
    dd=DB('contet.db')
    all = dd.queryDB('1')
    article=dict.fromkeys(['title','content'])
    for url in all:
        url=url[2]
        try:
            article=page.parse(url)
        except:
            logging.info(traceback.print_exc())
        dd.insertDB(article)
    
    wordFig=WordC()
    
    