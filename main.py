import requests
import pandas as pd
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit
# http://www.google.com/finance/getprices?i=60&p=10d&f=d,o,h,l,c,v&df=cpct&q=IBM

def f(x,a,b):
    return  a*x+b


symbol = input("Enter the symbol to graph:")

interval = 1 # minute(s)
interval = str(interval*60)

lookback = "1" # day(s)

raw = requests.get("http://www.google.com/finance/getprices?i="+interval+"&p="+lookback+"d&f=c&df=cpct&q="+symbol).text
raw = raw.split()[7:]

data = pd.DataFrame(raw)
data = data.astype("float")
data["price"] =  data[0]
del data[0]


if len(data["price"] >= 60):  data["price"] = data["price"][-60:]


data["mean"] = pd.expanding_mean(data["price"])
data["vol"] = pd.expanding_std(data["price"])

x = range(len(data["price"][-60:]))
y = data["price"][-60:].values

A,B = curve_fit(f,x,y)

if A[0] < 0 : print("downtrend")
else: print("uptrend")

plt.figure(1)

ax1 = plt.subplot(2,1,1)
plt.plot(data["price"])
plt.plot(data["mean"])


ax2 = plt.subplot(2,1,2)
plt.plot(data["vol"])
plt.plot(pd.rolling_mean(data["vol"],5))


plt.show()
