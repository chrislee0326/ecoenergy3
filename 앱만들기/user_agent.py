import requests


url = "https://new.kpx.or.kr/powerSource.es?mid=a10606030000&device=chart"
headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"}
res = requests.get (url, headers = headers)
res.raise_for_status()

soup = BeautifulSoup(res.text, "lxml")
#print(res.text)
#with open("elect.html", "w", encoding="utf8") as f:
    #f.write(res.text)
print(soup.find(attrs={"class":"conTable tdCenter"}))