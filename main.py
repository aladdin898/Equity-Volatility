import requests
import pandas as pd
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit
# http://www.google.com/finance/getprices?i=60&p=10d&f=d,o,h,l,c,v&df=cpct&q=IBM

# Linear function for linear regression
def f(x,a,b):
    return  a*x+b


symbol = input("Enter the symbol to graph:")

# Let's set up the URL for our GET request
interval = 1 # minute(s)
interval = str(interval*60)

lookback = "1" # day(s)

raw = requests.get("http://www.google.com/finance/getprices?i="+interval+"&p="+lookback+"d&f=c&df=cpct&q="+symbol).text

# Take the data and put it into a DataFrame
raw = raw.split()[7:]

data = pd.DataFrame(raw)
data = data.astype("float")
data["price"] =  data[0]
del data[0]

# We only need 60 minutes worth of data
if len(data["price"] >= 60):  data["price"] = data["price"][-60:]

# Columns for expanding mean and standard deviation
data["mean"] = pd.expanding_mean(data["price"])
data["vol"] = pd.expanding_std(data["price"])

# Linear regression on price data
x = range(len(data["price"][-60:]))
y = data["price"][-60:].values

A,B = curve_fit(f,x,y)

# Print the trend to the console
if A[0] < 0 : print("downtrend")
else: print("uptrend")

# Plot window
plt.figure(1)

# Plot for the price and its moving average
ax1 = plt.subplot(2,1,1)
plt.plot(data["price"])
plt.plot(data["mean"])

# Plot for the standard deviation and its moving average
ax2 = plt.subplot(2,1,2)
plt.plot(data["vol"])
plt.plot(pd.rolling_mean(data["vol"],5))

# Done !
plt.show()
