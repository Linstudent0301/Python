import requests, datetime as dt
from bs4 import BeautifulSoup
from datetime import datetime


def Respon(url):
    headers = {"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36"}
    cookies = {'over18': '1'}
    r = requests.get(url, cookies=cookies, headers=headers)
    soup = BeautifulSoup(r.text, 'lxml')
    return soup


def Post_Date(url, y1, m1, d1, y2, m2, d2, file):
    soup = Respon(url)
    date1 = soup.select("div.article-metaline span.article-meta-value")
    date2 = datetime.strptime(date1[2].text, "%a %b %d %H:%M:%S %Y")  
    if (date2 >= datetime(y1, m1, d1)) and (date2 <= datetime(y2, m2, d2)):
        tag = soup.select('div.push span.f3.push-content')
        for t in tag:
            file.write(t.text.replace(": ", "")+"\n")
        return True

    elif date2 > datetime(y2, m2, d2):  
        return "超過"

    elif date2 < datetime(y1, m1, d1):  
        return "低於"

    
def PTT(y1, m1, d1, y2, m2, d2, Kanban, search, filename):
    file = open("{}.txt".format(str(filename)), 'w', encoding='UTF-8')
    T1   = True
    page = 1
    while T1:
        soup = Respon("https://www.ptt.cc/bbs/{}/search?page={}&q={}".format(Kanban, str(page), search))
        T2   = True
        link =  1
        while T2:
            url = "https://www.ptt.cc" + soup.select("div.title a")[link - 1].get('href')
            post = Post_Date(url, y1, m1, d1, y2, m2, d2, file)
            if (post == True) or (post == "超過"):
                link += 1
            elif (post == "低於"):
                T1 = False
                T2 = False
            if (link == 20 + 1):
                T2 = False
        page += 1  
    file.close()
