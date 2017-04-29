#coding:utf-8
import sqlite3

class DB:
    'save items parsed from sss'
    def __init__(self,db='c:/temp/content1.db'):
        self.__conn = sqlite3.connect(db)
        self.__cur=self.__conn.cursor()
        self.createDB()
        #if not (u'sc',) in self.__cur.execute('select name from sqlite_master'):
        #    self.createDB()
    def createDB(self):
        self.__cur.execute('''
            create table if not exists sc(
            title varchar(50) primary key,
            temp varchar(20),
            href text(50),
            tag varchar(20),
            content text
            )        
        ''')
        self.__conn.commit()
        
    def insertDB(self,dict):
        query='insert into sc values (?,?,?,?,?);'
        key=['title','temp','href','tag','content']
        try:
            self.__cur.execute(query,map(lambda x:dict.get(x),key) )
        except sqlite3.IntegrityError:
            self.updateDB(dict)    
        self.__conn.commit()
        
    def queryDB(self,condition):
        query='select * from sc where %s;'% condition
        self.__cur.execute(query)
        # for row in self.__cur.fetchall():
            # print row
        return self.__cur.fetchall()
    
    def updateDB(self,dict):#dict.get("content")
        query='update sc set content=%r where title=%r'%\
            (dict.get("content").encode('utf-8'),dict.get("title").encode('utf-8'))
        
        try:
            self.__cur.execute(query)
        except sqlite3.OperationalError,e:
            # name =dict.get("title").encode('utf-8')+'.txt'
            # with open(name,'w') as f:
                # f.write(dict.get("content").encode('utf-8'))
            pass
            
        self.__conn.commit()
    
    def closeDB(self):
        self.__conn.close()
        
        
if __name__=='__main__':
    a=['major report prompts warnings that the arctic is unravelling,Home,https://www.scientificamerican.com/article/major-report-prompts-warnings-that-the-arctic-is-unravelling/,C"cc"c,66666666"66666666"66666666666',
    "this fantastic idea for a circular runway is sadly going nowhere,Home,https://www.scientificamerican.com/article/this-fantastic-idea-for-a-circular-runway-is-sadly-going-nowhere/,Eng5445,sdf'asd'fa's;'ffa"]
    key=['title','temp','href','tag','content'] 
    dd=  DB()
    for it in a:
        d={k:v for k,v in zip(key,it.split(','))}
        dd.insertDB(d)
        
    dd.queryDB('temp=="Home"')    
        
        