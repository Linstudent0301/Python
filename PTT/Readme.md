# 爬取PTT鄉民的留言
> [time=Sun, Jan 5, 2020 11:21 PM]
> [TOC]
### 載入模組
```python
import requests, datetime as dt
from bs4 import BeautifulSoup
from datetime import datetime
```

### Respon
```python=
def Respon(url):
    headers = {"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36"}
    cookies = {'over18': '1'}#有些看板有年齡限制
    r = requests.get(url, cookies=cookies, headers=headers)
    soup = BeautifulSoup(r.text, 'lxml')#使用lxml解析器
    return soup
```

### Post_Date

```python=
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
```
> ##### %a=星期(英文縮寫)、%b=月份(英文縮寫)、%Y=西元年(四位數)
> ![](https://i.imgur.com/zl5pwER.png)
```python
date2 = datetime.strptime(date1[2].text, "%a %b %d %H:%M:%S %Y") 
```
> ##### 判斷文章日期是否在規定的範圍內
```python
if (date2 >= datetime(y1, m1, d1)) and (date2 <= datetime(y2, m2, d2)) 
```
> ##### 條件符合(日期)就把留言寫入文件
```python
tag = soup.select('div.push span.f3.push-content')#返回列表
for t in tag:
    file.write(t.text.replace(": ", "")+"\n")
```
### PTT
```python=
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
```

> ##### "w"模式開啟文件、將編碼方式設定為萬國碼(中文)
```python
file = open("{}.txt".format(str(filename)), 'w', encoding='UTF-8')
```

> ##### Kanban=看板名稱、page=目前頁數、search=要搜尋的標題
```python
soup = Respon("https://www.ptt.cc/bbs/{}/search?page={}&q={}".format(Kanban, str(page), search))
```
> ##### 在目前的頁數下爬取第1篇、第2篇、第3篇文章的網址以此類推(每頁最多20篇)
```python
url = "https://www.ptt.cc" + soup.select("div.title a")[link - 1].get('href')
```
> ##### 判斷發文日期是否在規定的範圍內
```python
post = Post_Date(url, y1, m1, d1, y2, m2, d2, file)
```
> ##### PTT發文日期的排序方式是由大到小
```python
if (post == True) or (post == "超過"):
    link += 1
```
> ##### 發文日期低於規定範圍，所以將T1,T2設為False，結束迴圈
```python
elif (post == "低於"):
    T1 = False
    T2 = False
```
> ##### 這頁已經爬了20篇文章，結束迴圈
```python
if (link == 20 + 1):
    T2 = False
```
> ##### 爬下一頁
```python
page += 1  
```
> ##### 關閉文件
```python
file.close()
```
### 測試
```python
PTT(2019, 12, 1, 2020, 2, 1, "Gossiping", "跨年", "PTT跨年")
```
