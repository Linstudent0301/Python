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
