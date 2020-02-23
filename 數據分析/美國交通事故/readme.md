# 美國交通事故數據分析
##### 資料來源：[kaggle](https://www.kaggle.com/sobhanmoosavi/us-accidents)

### 每小時(24)的事故量
![](https://i.imgur.com/g13ldbl.png)

* 上、下班時間最容易發生事故。
* 上、下班時間的車流量本來就會很多，所以在這個時段可能要採取一些車輛引流的措施，才能有效減少事故量。

----

### 每月的事故量
![](https://i.imgur.com/yj4t0dz.png)
2019年10、12月事故量最多(都在10萬上下)

----

### 事故發生時的天氣狀況
![](https://i.imgur.com/o7XawzC.png)
天氣明朗的時候最容易發生事故

----

### 各州事故量統計
![](https://i.imgur.com/uth84OT.png)

事故量前三名的州分別是CA、TX、FL，其中CA有著高達60萬的事故量而且跟TX、FL有40萬的差距


----

### 事故的嚴重程度
![](https://i.imgur.com/zznwIOD.png)

----

### 白天跟晚上的事故量
![](https://i.imgur.com/tBp7g67.png)

白天最容易發生事故

----

### 平日跟假日的事故量
![](https://i.imgur.com/4yoFHg7.png)

平日最容易發生事故

----

### 各時區的事故量
![](https://i.imgur.com/MicmCcy.png)

東岸時區(1,277,186)、太平洋時區(805,117)、中部時區(727,147)、山地時區(161,721)，  
美國沿海地區最容易發生事故

---
```
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime as dt

# ============================================

df = pd.read_csv("US_Accidents_Dec19.csv")

# ============================================

df['Date_Time'] = pd.to_datetime(df['Start_Time'])
del_index = df[df['Date_Time'] < '2016-01'].index
df = df.drop(del_index)

# ============================================

df['Hour'] = df['Date_Time'].dt.hour
Hour = df['Hour'].value_counts().sort_index()
plt.bar(Hour.index, Hour.values)
plt.xticks(Hour.index)

# ============================================

df['Date'] = df['Date_Time'].dt.strftime("%y-%m")
Date = df['Date'].value_counts().sort_index()
plt.bar(Date.index, Date.values)
plt.xticks(rotation=90)

# ============================================

Weather = df['Weather_Condition'].value_counts(ascending=True)[-5:]
plt.barh(Weather.index, Weather.values)

# ============================================

State = df['State'].value_counts(ascending=True)[-10:]
plt.barh(State.index, State.values)

# ============================================

Severity = df['Severity'].value_counts()
plt.pie(x=Severity.values, labels=Severity.index, autopct='%1.2f%%')

# ============================================

Rise_Set = df['Sunrise_Sunset'].value_counts()
plt.pie(x=Rise_Set.values, labels=Rise_Set.index, autopct='%1.1f%%')

# ============================================

Week = list(df['Date_Time'].dt.dayofweek.value_counts().sort_index())
work = 0
holiday = 0
for i in range(len(Week)):
    if i > len(Week) - 3:
        holiday += Week[i]
    else:  #平日
        work += Week[i]
plt.pie(x=[work, holiday], labels=['Weekday', 'Holiday'], autopct='%1.0f%%')

# ============================================

Timezone = df['Timezone'].value_counts()
plt.bar(Timezone.index, Timezone.values)

```
