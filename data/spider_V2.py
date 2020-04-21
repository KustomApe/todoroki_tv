from urllib.request import urlopen
import pandas as pd
url = 'https://fx.minkabu.jp/indicators'
f = urlopen(url)
html = f.read()
print(html)

df = pd.io.html.read_html(html)
print(df)

dfs = pd.read_html(url, match='')