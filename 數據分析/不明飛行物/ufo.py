import requests
import urllib.request
import numpy as np
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
from bs4                    import BeautifulSoup
from urllib.request         import urlopen
from datetime               import datetime, date
from mpl_toolkits.basemap   import Basemap
from matplotlib.colors      import rgb2hex, Normalize
from matplotlib.patches     import Polygon
from matplotlib.colorbar    import ColorbarBase
from wordcloud import WordCloud


# ===========================================

def use_proxy(proxy_addr, url):
    proxy = urllib.request.ProxyHandler({'https': proxy_addr})
    opener = urllib.request.build_opener(proxy, urllib.request.HTTPHandler)
    urllib.request.install_opener(opener)
    r = urllib.request.urlopen(url).read()
    return r

r = use_proxy('194.167.44.91:80',"http://www.nuforc.org/webreports/ndxevent.html")
soup = BeautifulSoup(r, "html5lib")

df = pd.DataFrame()
tag = soup.select("font a")
url = "http://www.nuforc.org/webreports/"
for t in tag:
    if t == tag[len(tag)-1]:
        pass
    else:
        date = datetime.strptime(t.text[3:] + t.text[:2], "%Y%m")
        if date >= datetime(1940, 1, 1) :
            table = pd.read_html(url + t.get('href'))[0]
            df = pd.concat([df,table])
            df.to_excel("UFO.xlsx", index=False)

# ============================================

df = pd.read_excel("UFO.xlsx").drop("Posted", axis=1)
df["Date / Time"] = pd.to_datetime(df["Date / Time"])
for i in range(len(df)):
    over = df["Date / Time"][i]
    if over > datetime(2040, 1, 1):
        df["Date / Time"][i] = over.replace(year=over.year - 100)

State1 = df["State"].value_counts()
State1 = [[State1.index[i], State1.values[i]] for i in range(len(State1))]
State2 = []
State3 = []
abbr = pd.read_excel("US-50.xlsx")
abbr = pd.Series(abbr["Name"].values, index=abbr["Abbreviation"])

for i in range(len(abbr)):
    for j in range(len(State1)):
        if abbr.index[i] == State1[j][0]:  #篩選出美國50州
            State3.append([State1[j][0], State1[j][1]])  #柱狀圖
            State1[j][0] = abbr.values[i].replace(" /u3000", "")
            State2.append(State1[j])
State2 = dict(State2)

# ============================================

df["Year"] = df["Date / Time"].dt.year
Year = df["Year"].value_counts().sort_index()
plt.plot(Year.index, Year.values)
plt.title("Year")
print(df["Year"].value_counts())

# ============================================

df["Month"] = df["Date / Time"].dt.month
Month = df["Month"].value_counts().sort_index()
plt.subplot(1,2,1)
plt.bar(Month.index, Month.values)
plt.xticks(Month.index, fontsize = 9)
plt.title("Month")

# ============================================

df["Hour"] = df["Date / Time"].dt.hour
Hour = df["Hour"].value_counts().sort_index()
plt.subplot(1, 2, 2)
plt.bar(Hour.index, Hour.values)
plt.xticks(Hour.index, fontsize = 9)
plt.title("Hour")

# ============================================

State3 = pd.Series(dict(State3)).sort_values()[-10:]
plt.barh(State3.index, State3.values)
plt.title("State")

# ============================================

shape = df["Shape"].value_counts(ascending = True)[-10:]
plt.barh(shape.index, shape.values)
plt.title("Shape")

# ============================================

s = ""
for i in range(len(df)):
    s += str(df['Summary'][i])
wordcolud = WordCloud(collocations=False,
                      width=1000,
                      height=800,
                      background_color="white").generate(s)
plt.imshow(wordcolud, interpolation='bilinear')
plt.axis("off")

# ============================================

fig, axs = plt.subplots(figsize=(8, 5))
m = Basemap(llcrnrlon=-119,
            llcrnrlat=20,
            urcrnrlon=-64,
            urcrnrlat=49,
            projection='lcc',
            lat_1=33,
            lat_2=45,
            lon_0=-95)

m.readshapefile('st99_d00','state',color='gray')

colors = {}
statenames = []
for infodict in m.state_info:
    name = infodict['NAME']
    statenames.append(name)
    if name not in ['District of Columbia', 'Puerto Rico']:
        qua = State2[name]  #ufo的出現的次數
        colors[name] = plt.cm.hot_r((qua) / (10000))[:3]  #紅綠藍的比例

for i, seg in enumerate(m.state):
    if statenames[i] not in ['District of Columbia', 'Puerto Rico']:
        color = rgb2hex(colors[statenames[i]])  #顏色的比例轉色碼表
        poly = Polygon(seg, facecolor=color, edgecolor=color)  #填滿多邊形顏色
        axs.add_patch(poly)

cax = fig.add_axes([0.9, 0.1, 0.02, 0.8])  #左,下,寬度,高度
ColorbarBase(ax=cax, cmap=plt.cm.hot_r, norm=Normalize(vmin=0, vmax=10000))
fig.suptitle('State',  fontsize = 18, x = 0.45)
