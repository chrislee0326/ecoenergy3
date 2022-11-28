import requests 
from bs4 import BeautifulSoup

url = "https://new.kpx.or.kr/powerSource.es?mid=a10606030000&device=chart"
headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"}
res = requests.get (url, headers = headers)
res.raise_for_status()
soup = BeautifulSoup(res.text, "lxml")

time = (soup.find("tbody"))

all = time.tr
real = all.td
another = real.next_sibling.next_sibling

while True:  
    if str(another) == '<td>0</td>':
        all = all.previous_sibling.previous_sibling
        real = all.td
        another = real.next_sibling.next_sibling
        gas = another.next_sibling.next_sibling
        eco = gas.next_sibling.next_sibling
        coal = eco.next_sibling.next_sibling
        nuclear = coal.next_sibling.next_sibling
        break
    else:
        all = all.next_sibling.next_sibling
        real = all.td
        another = real.next_sibling.next_sibling
        continue


import re

another2 = re.findall("-?\d+", str(another));another2 = another2[0]
gas = re.sub(r'[^0-9]', '', str(gas))
eco = re.sub(r'[^0-9]', '', str(eco))
coal = re.sub(r'[^0-9]', '', str(coal))
nuclear = re.sub(r'[^0-9]', '', str(nuclear))
total = int(another2) + int(gas) + int(eco) + int(coal) + int(nuclear)

rate1 = int(eco)/total
rate2 = int(eco)/total+int(gas)/total
rate3 = int(eco)/total+int(nuclear)/total
rate4 = int(eco)/total+int(gas)/total+int(nuclear)/total
