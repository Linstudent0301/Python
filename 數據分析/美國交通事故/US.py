import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime as dt

# ============================================
# 讀取數據
df = pd.read_csv("C:\Users\霖\Desktop\數據分析\美國交通事故\美國交通事故1.csv")

# ============================================
# 數據清洗
df['Date_Time'] = pd.to_datetime(df['Start_Time'])
del_index = df[df['Date_Time'] < '2016-02'].index
df = df.drop(del_index)

# ============================================
# 事故量(時)
df['Hour'] = df['Date_Time'].dt.hour
Hour = df['Hour'].value_counts().sort_index()
plt.bar(Hour.index, Hour.values)
plt.xticks(Hour.index)

# ============================================
# 事故量(月)
df['Date'] = df['Date_Time'].dt.strftime("%y-%m")
Date = df['Date'].value_counts().sort_index()
plt.bar(Date.index, Date.values)
plt.xticks(rotation=90)

# ============================================
# 發生事故當時的天氣狀況
Weather = df['Weather_Condition'].value_counts(ascending=True)[-5:]
plt.barh(Weather.index, Weather.values)
plt.pie(x=Weather.values, labels=Weather.index, autopct='%1.1f%%')

# ============================================
# 每個州的事故量
State = df['State'].value_counts(ascending=True)[-10:]
plt.barh(State.index, State.values)
plt.pie(x=State.values, labels=State.index, autopct='%1.1f%%')

# ============================================
# 事故的嚴重程度
Severity = df['Severity'].value_counts()
plt.bar(np.arange(len(Severity)), Severity.values)
plt.xticks(np.arange(len(Severity)), Severity.index)
plt.pie(x=Severity.values, labels=Severity.index, autopct='%1.1f%%')

# ============================================
# 白天、晚上
Rise_Set = df['Sunrise_Sunset'].value_counts()
plt.pie(x=Rise_Set.values, labels=Rise_Set.index, autopct='%1.0f%%')

# ============================================
# 平日、假日
Week = list(df['Date_Time'].dt.dayofweek.value_counts().sort_index())
work = 0
holiday = 0
for i in range(len(Week)):  #0~4平日 5~6假日
    if i > len(Week) - 3:  #假日
        holiday += Week[i]
    else:  #平日
        work += Week[i]
plt.pie(x=[work, holiday], labels=['Weekday', 'Holiday'], autopct='%1.0f%%')

# ============================================
# 各時區的事故量
Timezone = df['Timezone'].value_counts()
plt.bar(Timezone.index, Timezone.values)
plt.pie(x=Timezone.values, labels=Timezone.index, autopct='%1.1f%%')
