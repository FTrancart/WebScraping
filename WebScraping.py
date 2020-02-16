from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np

names=[]
prices=[]
changes=[]
percentChanges=[]
 
currenciesUrl = "https://in.finance.yahoo.com/currencies"
data = requests.get(currenciesUrl)
soup = BeautifulSoup(data.text)
 
counter = 40
for i in range(40, 404, 14):
    for listing in soup.find_all('tr', attrs={'data-reactid':i}):
        for name in listing.find_all('td', attrs={'data-reactid':i+3}):
            names.append(name.text)
        for price in listing.find_all('td', attrs={'data-reactid':i+4}):
            prices.append(price.text)
        for change in listing.find_all('td', attrs={'data-reactid':i+5}):
            changes.append(change.text)
        for percentChange in listing.find_all('td', attrs={'data-reactid':i+7}):
            percentChanges.append(percentChange.text)
            
percentChangesSorted = sorted([percentChanges[x].replace("%", "") for x in range(len(percentChanges))], key=float, reverse = True)
index = np.argsort([float(el.replace("%", "")) for el in percentChanges])[::-1]

df = pd.DataFrame({"Names": [names[x] for x in index], "Prices": [prices[x] for x in index], "Change": [changes[x] for x in index], "% Change": percentChangesSorted})
df.to_csv('YahooCurrencies.csv', index=False, encoding='utf-8', sep=';')
